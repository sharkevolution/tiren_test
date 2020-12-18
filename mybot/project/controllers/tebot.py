# -*- coding: UTF-8 -*-

# https://unicode.org/emoji/charts/full-emoji-list.html#1f600
# https://apps.timwhitlock.info/emoji/tables/unicode
# https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py
# https://habr.com/ru/company/ruvds/blog/325522/
# https://www.networkworld.com/article/3276349/copying-and-renaming-files-on-linux.html


import bottle
from bottle import view, request, redirect

import os
import json
import requests
import logging
import redis
import msgpack

from mybot.project.controllers import planner
from mybot.project.controllers import dredis
from mybot.project.controllers import settings_user
from mybot.project.controllers import chtime


def callback_hello_ok(data, text):
    try:
        message = {"callback_query_id": data['callback_query']['id'], "text": text, "cache_time": 0}
        r = requests.post(bot.api_answer, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200
    except Exception as ex:
        logging.error(ex)
    return r


def user_start_update(chat_id, _from):
    """ Start and Updater user profile """
    if not bot.users.get(chat_id):
        # Add info about User
        clu = User(chat_id)
        clu.from_id = _from['id']
        clu.first_name = _from['first_name']
        clu.last_name = _from['last_name']

        clu.put_redis_info()
        bot.users[User(chat_id).__name__] = clu

    cs = bot.users[chat_id]
    csdata = cs.get_redis()
    if csdata.get('last_message_id'):
        cs.last_message_id = csdata['last_message_id']
        cs.from_id = csdata['from_id']
        cs.first_name = csdata['first_name']
        cs.last_name = csdata['last_name']

    bot.users[chat_id] = cs
    bot.last_chat = chat_id  # Active chat

    return cs


def handler_response_ok(resp):
    """ Обработчик успешного ответа от сервера """
    data = resp.json()
    if isinstance(data, dict):
        if data['result'] == True:
            pass
        elif data['result'].get('message_id'):
            mi = data['result'].get('message_id')
            # logging.info(data)
            chat_id = data['result']['chat']['id']
            cs = bot.users[chat_id]
            cs.put_redis_last_message_bot(mi)


class User:
    def __init__(self, chat_id):
        self.__name__ = chat_id
        self.from_id = None
        self.first_name = None
        self.last_name = None
        self.combination = []  # Time text value
        self.adr = []  # List of store addresses
        self.delivery = []  # List of carriers
        self.weight = []  # Capacity
        self.last_message_id = 0
        self.last_bot_id = 0
        self.pull_user_commands = {}  # Additional set user commands
        self.current_task = {}  # Current task
        self.redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    def get_redis(self):

        res = {}
        if self.redisClient.exists(self.__name__):
            res = msgpack.unpackb(self.redisClient.get(self.__name__))
            # logging.info(res)
        return res

    def put_redis_last_message_id(self, data):

        self.last_message_id = data['message']['from']['id']
        if base_keys := self.get_redis():
            base_keys['last_message_id'] = self.last_message_id
        else:
            base_keys = {'last_message_id': self.last_message_id}
        new_pack = msgpack.packb(base_keys)
        self.redisClient.set(self.__name__, new_pack)

    def put_redis_last_message_bot(self, mi):

        self.last_bot_id = mi

        if base_keys := self.get_redis():
            base_keys['last_bot_id'] = self.last_bot_id
        else:
            base_keys = {'last_bot_id': self.last_bot_id}
        new_pack = msgpack.packb(base_keys)
        self.redisClient.set(self.__name__, new_pack)

    def put_redis_info(self):

        base_keys = {'from_id': self.from_id,
                     'first_name': self.first_name,
                     'last_name': self.last_name}
        new_pack = msgpack.packb(base_keys)
        self.redisClient.set(self.__name__, new_pack)

    def create_task(self):
        self.current_task = {'shop': None, 'delivery': None, 'weight': None, 'dlv_time': None,
                             'status_send': 'pending'}

    def put_task(self):
        pass

    def __repr__(self):
        return self.__name__


class Bot:
    """ Bot token """

    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.api_answer = f'https://api.telegram.org/bot{self.token}/answerCallbackQuery'
        self.api_edit_message = f'https://api.telegram.org/bot{self.token}/editMessageText'
        self.api_get_updates = f'https://api.telegram.org/bot{self.token}/getUpdates'
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        self.users = {}  # List of users
        self.dict_init = {}  # Custom logic

        self.last_id = 0  # Last ID telegram (not message)
        self.last_chat = None  # Last chat
        self.tasks = {}  # Dict of users tasks


class Dispatcher:
    """ handler messages command """

    def __init__(self, bot):
        self.bot = bot
        self.commands = None
        self.pull_message_commands = {}
        self.pull_callback_commands = {}

    def message_handler(self, commands):
        def decorator(fn):
            for b in commands:
                self.pull_message_commands[b] = fn

            def decorated2(*args, **kwargs):
                self.commands = commands
                return fn(*args, **kwargs)

            decorated2.__name__ = fn.__name__
            return decorated2

        return decorator

    def callback_handler(self, commands):
        def decorator(fn):
            for b in commands:
                self.pull_callback_commands[b] = fn

            def decorated2(*args, **kwargs):
                self.commands = commands
                return fn(*args, **kwargs)

            decorated2.__name__ = fn.__name__
            return decorated2

        return decorator


# ********************************************************
API_TOKEN = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


# ********************************************************

@dp.message_handler(commands=[])
def dynamic_weight(data, ord=None):
    # logging.info('Weight')
    tunnel = data['message']['chat']['id']
    result_text = 'Грузоподъемность'
    reply_markup, chat_user = settings_user.template_weight(bot.dict_init, bot.users[tunnel])

    # Update commands wrapper
    for b in chat_user.weight:
        chat_user.pull_user_commands[b] = keboard_bot

    chat_user.current_task['delivery'] = ord
    bot.users[tunnel] = chat_user

    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.message_handler(commands=[])
def dynamic_delivery(data, ord=None):
    # logging.info('Delivery')
    tunnel = data['message']['chat']['id']
    result_text = 'Выберите перевозчика'
    reply_markup, chat_user = settings_user.template_delivery(bot.dict_init, bot.users[tunnel])

    # Update commands wrapper
    for b in chat_user.delivery:
        chat_user.pull_user_commands[b] = dynamic_weight

    chat_user.current_task['shop'] = ord
    bot.users[tunnel] = chat_user

    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.callback_handler(commands=['region_arrived', ])
def region_arrived(data, ord=None):
    callback_hello_ok(data, 'Переход на время прибытия')

    tunnel = data['callback_query']['message']['chat']['id']
    result_text = 'Выберите адрес из списка'
    reply_markup, chat_user = settings_user.template_shops(bot.dict_init, bot.users[tunnel])

    # Update commands wrapper
    for b in chat_user.adr:
        chat_user.pull_user_commands[b] = dynamic_delivery
    chat_user.create_task()  # Create task
    bot.users[tunnel] = chat_user

    # logging.info('Region arrived')
    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}

    return message, bot.api_url


@dp.callback_handler(commands=['ent_list'])
def enter_to_list(data, ord=None):
    r = callback_hello_ok(data, 'ok!')
    chat_id = data['callback_query']['message']['chat']['id']

    if tmp_list := bot.tasks.get(chat_id):
        html_list = []

        for ts in tmp_list:
            shop = ts['shop']
            dlv = ts['delivery']
            wt = ts['weight']
            st = ts['dlv_time']

            tmp_text = ' | '.join([shop, dlv, wt, st, ])

            html_list.append(tmp_text)

        result_text = '\n'.join(html_list)

        res = {'chat_id': chat_id, 'text': result_text, 'parse_mode': 'HTML'}
    else:
        result_text = f"Список пуст, заполните время"
        res = {'chat_id': chat_id, 'text': result_text, }

    logging.info(res)
    return res, bot.api_url



@dp.callback_handler(commands=['ent_shops'])
def enter_to_shops(data, ord=None):
    r = callback_hello_ok(data, 'ok!')
    chat_id = data['callback_query']['message']['chat']['id']

    chat_user = bot.users[chat_id]
    chat_user.create_task()  # Clear current task
    bot.users[chat_id] = chat_user

    tunnel = data['callback_query']['message']['chat']['id']
    result_text = 'Выберите адрес из списка'
    reply_markup, chat_user = settings_user.template_shops(bot.dict_init, bot.users[tunnel])

    # Update commands wrapper
    for b in chat_user.adr:
        chat_user.pull_user_commands[b] = dynamic_delivery
    chat_user.create_task()  # Create task
    bot.users[tunnel] = chat_user

    # logging.info('Region arrived')
    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}

    return message, bot.api_url



@dp.callback_handler(commands=['ent_one', 'ent_two', 'ent_three', 'ent_four', 'ent_five',
                               'ent_six', 'ent_seven', 'ent_eight', 'ent_nine', 'ent_zero',
                               'ent_colon'])
def enter(data, ord=None):
    r = callback_hello_ok(data, 'ok!')
    chat_id = data['callback_query']['message']['chat']['id']

    chat_user = bot.users[chat_id]
    # Edit Message
    check_list = chtime.check(ord, chat_user.combination)
    my_test = ''.join(check_list)
    my_comb = ''.join(chat_user.combination)
    if my_test == my_comb:
        return {}, {}
    else:
        chat_user.combination = check_list
        if len(chat_user.combination) == 5:
            chat_user.current_task['dlv_time'] = my_test
            logging.info(chat_user.current_task)

            val = 0
            for b in chat_user.current_task:
                if not chat_user.current_task[b] is None:
                    val += 1
            if val == 5:
                # Add tasks to dict from send
                if bot.tasks.get(chat_id):
                    tmp_ = bot.tasks[chat_id]
                    tmp_.append(chat_user.current_task)
                    logging.info(bot.tasks)
                else:
                    bot.tasks[chat_id] = [chat_user.current_task, ]
                    logging.info(bot.tasks)

    base_keys = chat_user.get_redis()
    chat_user.last_message_id = base_keys['last_bot_id']

    curl = bot.api_edit_message
    message = {'chat_id': chat_id, 'message_id': chat_user.last_message_id, 'text': my_test}

    logging.info('EDIT Message')
    logging.info(chat_user.last_message_id)

    try:
        r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200

        handler_response_ok(r)  # Обработчик ответа

    except Exception as ex:
        logging.info(r)
        logging.error('Error' + str(ex))

    return {}, {}


@dp.message_handler(commands=['/idc', ])
def bind_bot(data, ord=None):
    tunnel = data['message']['chat']['id']
    message = {'chat_id': tunnel, 'text': data['message']['chat']['id']}
    return message, bot.api_url


@dp.message_handler(commands=['/bc', ])
def keboard_bot(data, ord=None):

    tunnel = data['message']['chat']['id']
    result_text = 'Введите время прибытия'
    reply_markup = settings_user.template_engineer_mode()
    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}

    r = requests.post(bot.api_url, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    chat_user = bot.users[tunnel]
    chat_user.current_task['weight'] = ord

    # Input pass
    chat_user.combination = []
    bot.users[tunnel] = chat_user

    result_text = "Input key: "
    message = {'chat_id': data['message']['chat']['id'], 'text': result_text}

    try:
        r = requests.post(bot.api_url, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200
        handler_response_ok(r)  # Ловушка для получения ид сообщения от бота

    except Exception as ex:
        logging.info(r)
        logging.error('Error' + str(ex))

    return {}, {}


@dp.message_handler(commands=['/start', ])
def start_bot(data, ord=None):
    tunnel = data['message']['chat']['id']
    result_text = 'Приступим к работе'
    reply_markup = settings_user.template_start()
    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


def dummy_message(data):
    """ Заглушка для message """
    text = data['message'].get('text')
    result_text = f"Функция [{text}] в разработке."
    res = {'chat_id': data['message']['chat']['id'], 'text': result_text}
    return res, bot.api_url


def dummy_callback(data):
    """ Заглушка для callback_query """

    planner.start_proc()  # Run planner in different process
    logging.info("I am!")

    text = data['callback_query']['data']
    result_text = f"Функция [ {text} ] в разработке."
    res = {"callback_query_id": data['callback_query']['id'], "text": result_text, "cache_time": 3}
    return res, bot.api_answer


@bottle.route('/api/v1/echo', method='POST')
def do_echo():
    """ Main """

    message = {}
    curl = None

    dredis.variable_init(bot)  # get or set settings users regions to bot.dict_init
    data = request.json
    # logging.info(data)

    if bot.last_id < data['update_id']:
        # Отсекаем старые сообщения если ид меньше текущего
        bot.last_id = data['update_id']

        if data.get('callback_query'):
            # curl = bot.api_answer
            user_start_update(data['callback_query']['message']['chat']['id'], data['callback_query']['from'])

            if ord := data['callback_query'].get('data'):
                if exec_func := dp.pull_callback_commands.get(ord):
                    message, curl = exec_func(data, ord)
                else:
                    message, curl = dummy_callback(data)

        if data.get('message'):
            # curl = bot.api_url
            if ord := data['message'].get('text'):
                cs = user_start_update(data['message']['chat']['id'], data['message']['from'])
                cs.put_redis_last_message_id(data)
                bot.users[cs.__name__] = cs

                # logging.info(cs.pull_user_commands)
                if exec_func := cs.pull_user_commands.get(ord):
                    message, curl = exec_func(data, ord)
                elif exec_func := dp.pull_message_commands.get(ord):
                    # logging.info(ord)
                    message, curl = exec_func(data, ord)
                else:
                    message, curl = dummy_message(data)

        if message and curl:
            # logging.info(message)
            # logging.info(curl)
            try:
                r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
                assert r.status_code == 200
                # logging.info(r.content)
                # handler_response_ok(r)  # Обработчик ответа

            except Exception as ex:
                logging.info(r)
                logging.error('Error' + str(ex))

    # logging.info('old_message')
    # logging.info(data)
