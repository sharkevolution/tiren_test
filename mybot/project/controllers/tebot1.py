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


def callback_hello_ok(data, text):
    try:
        message = {"callback_query_id": data['callback_query']['id'], "text": text, "cache_time": 3}
        r = requests.post(bot.api_answer, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200
    except Exception as ex:
        logging.error(ex)
    return r


def user_start_update(chat_id):
    """ Start and Updater user profile """
    if not bot.users.get(chat_id):
        bot.users[User(chat_id).__name__] = User(chat_id)

    cs = bot.users[chat_id]
    csdata = cs.get_redis()
    if csdata.get('last_message_id'):
        cs.last_message_id = csdata['last_message_id']

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
        self.first_name = None
        self.last_name = None
        self.combination = []
        self.adr = []  # Store addresses
        self.delivery = []  #
        self.weight = []  # Capacity
        self.last_message_id = 0
        self.last_bot_id = 0
        self.pull_user_commands = {}
        self.redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    def get_redis(self):

        res = {}
        if self.redisClient.exists(self.__name__):
            res = msgpack.unpackb(self.redisClient.get(self.__name__))
            logging.info(res)
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
        self.last_chat = None


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
    logging.info('Weight')
    tunnel = data['message']['chat']['id']
    result_text = 'Грузоподъемность'
    reply_markup, chat_user = settings_user.template_weight(bot.dict_init, bot.users[tunnel])

    # Update commands wrapper
    for b in chat_user.weight:
        chat_user.pull_user_commands[b] = keboard_bot
    bot.users[tunnel] = chat_user

    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.message_handler(commands=[])
def dynamic_delivery(data, ord=None):
    logging.info('Delivery')
    tunnel = data['message']['chat']['id']
    result_text = 'Выберите перевозчика'
    reply_markup, chat_user = settings_user.template_delivery(bot.dict_init, bot.users[tunnel])

    # Update commands wrapper
    for b in chat_user.delivery:
        chat_user.pull_user_commands[b] = dynamic_weight
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
    bot.users[tunnel] = chat_user

    # logging.info('Region arrived')
    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}

    return message, bot.api_url


@dp.callback_handler(commands=['ent_one', 'ent_two', 'ent_three', 'ent_four', 'ent_five',
                               'ent_six', 'ent_seven', 'ent_eight', 'ent_nine', 'ent_zero'])
def enter(data, ord=None):
    r = callback_hello_ok(data, 'ok!')
    chat_id = data['callback_query']['message']['chat']['id']

    number_key = {'ent_one': 1, 'ent_two': 2, 'ent_three': 3, 'ent_four': 4,
                  'ent_five': 5, 'ent_six': 6, 'ent_seven': 7, 'ent_eight': 8,
                  'ent_nine': 9, 'ent_zero': 0, 'ent_colon': ':'}

    valid_range = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0,
                   '08': 0, '09': 0, '1': 0, '2': 0, '10': 0, '11': 0, '12': 0,
                   '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0,
                   '20': 0, '21': 0, '22': 0, '23': 0}

    # Edit Message
    chat_user = bot.users[chat_id]

    tmp_list = chat_user.combination.copy()
    tmp_list.append(str(number_key[ord]))
    raw_text = ''.join(tmp_list)

    logging.info(raw_text)
    if valid_range.get(raw_text):
        chat_user.combination.append(':')
    else:
        if ':' in chat_user.combination:
            f = chat_user.combination.split(':')
            if len(f) == 1:
                if number_key[ord] > 5:
                    return {}, {}
            elif len(f) == 2:
                if number_key[ord] > 5:
                    return {}, {}
            else:
                return {}, {}

    chat_user.combination.append(str(number_key[ord]))
    my_test = ''.join(chat_user.combination)

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

    # Input pass
    chat_user = bot.users[tunnel]
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
            user_start_update(data['callback_query']['message']['chat']['id'])

            if ord := data['callback_query'].get('data'):
                if exec_func := dp.pull_callback_commands.get(ord):
                    message, curl = exec_func(data, ord)
                else:
                    message, curl = dummy_callback(data)

        if data.get('message'):
            # curl = bot.api_url
            if ord := data['message'].get('text'):
                cs = user_start_update(data['message']['chat']['id'])
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
            logging.info(message)
            # logging.info(curl)
            try:
                r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
                assert r.status_code == 200
                logging.info(r.content)
                # handler_response_ok(r)  # Обработчик ответа

            except Exception as ex:
                logging.info(r)
                logging.error('Error' + str(ex))

    # logging.info('old_message')
    # logging.info(data)
