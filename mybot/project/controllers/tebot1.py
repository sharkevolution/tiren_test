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
# import types

from mybot.project.controllers import planner
from mybot.project.controllers import dredis
from mybot.project.controllers import settings_user


DICT_INIT = {}
HANDLER_USER_ADR = {}
HANDLER_USER_DELIVERY = {}


def callback_hello_ok(data, text):
    try:
        message = {"callback_query_id": data['callback_query']['id'], "text": text, "cache_time": 3}
        r = requests.post(bot.api_answer, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200
    except Exception as ex:
        logging.error(ex)


class User:
    def __init__(self):
        self.user_messages_id = []
        self.user_first_name = None
        self.user_last_name = None
        self.user_combination = []

    def get_redis(self):
        pass


class Bot(User):
    """ Bot token """

    def __init__(self, token):

        super().__init__()

        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.api_answer = f'https://api.telegram.org/bot{self.token}/answerCallbackQuery'
        self.api_edit_message = f'https://api.telegram.org/bot{self.token}/editMessageText'
        self.api_get_updates = f'https://api.telegram.org/bot{self.token}/getUpdates'

        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
        self.last_id = 0  # последний ID telegram
        self.last_message_id = 0
        self.message_id_list = []


class Dispatcher(User):
    """ handler messages command """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.commands = None
        self.pull_message_commands = {}
        self.pull_callback_commands = {}
        self.pull_message_requests = {}
        self.bind_group = [['testroz', '/4523'], ]
        self.bind_groups = []  # Список разрешенных групп для обмена сообщениями

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


API_TOKEN = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


# @dp.callback_handler(commands=['region_arrived', ])
# def region_arrived(data):
#
#     callback_hello_ok(data, 'Выберите адрес')
#
#     tunel = data['callback_query']['message']['chat']['id']
#     result_text = 'Введите время прибытия и выберите перевозчика из списка'
#     reply_markup = settings_user.template_engineer_mode()
#     message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}
#
#     return message, bot.api_url


@dp.message_handler(commands=HANDLER_USER_ADR)
def bind_bot(data):
    tunel = data['message']['chat']['id']
    result_text = 'Выберите перевозчика'
    reply_markup = settings_user.template_delivery()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.callback_handler(commands=['region_arrived', ])
def region_arrived(data):

    callback_hello_ok(data, 'Переход на время прибытия')

    tunel = data['callback_query']['message']['chat']['id']
    result_text = 'Выберите адрес из списка'
    reply_markup = settings_user.template_shops()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}

    return message, bot.api_url


@dp.callback_handler(commands=['ent_one', 'ent_two', 'ent_three', 'ent_four', 'ent_five',
                               'ent_six', 'ent_seven', 'ent_eight', 'ent_nine', 'ent_zero'])
def enter(data):

    callback_hello_ok(data, 'ok!')

    # Edit Message
    bot.user_combination.append('1')
    my_test = ''.join(bot.user_combination)

    chat_id = data['callback_query']['message']['chat']['id']
    base_keys = dredis.get_redis_message(chat_id)

    logging.info(base_keys)
    last_message_id = base_keys['sms_id_last_bot']

    curl = bot.api_edit_message
    message = {'chat_id': data['callback_query']['message']['chat']['id'],
               'message_id': last_message_id,
               'text': my_test}

    logging.info('EDIT Message')
    logging.info(last_message_id)

    try:
        r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200

        handler_response_ok(r)  # Обработчик ответа

    except Exception as ex:
        logging.info(r)
        logging.error('Error' + str(ex))

    return {}, {}


@dp.message_handler(commands=['/idc', ])
def bind_bot(data):
    tunel = data['message']['chat']['id']
    message = {'chat_id': tunel, 'text': data['message']['chat']['id']}
    return message, bot.api_url


@dp.message_handler(commands=['/bc', ])
def keboard_bot(data):
    tunel = data['message']['chat']['id']
    result_text = 'Введите время прибытия и выберите перевозчика из списка'
    reply_markup = settings_user.template_engineer_mode()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}

    r = requests.post(bot.api_url, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    # Input pass
    bot.user_combination = []
    result_text = "Input key: "
    message = {'chat_id': data['message']['chat']['id'], 'text': result_text}

    return message, bot.api_url


@dp.message_handler(commands=['/start', ])
def start_bot(data):
    tunel = data['message']['chat']['id']
    result_text = 'Приступим к работе'
    reply_markup = settings_user.template_start()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.message_handler(commands=['Город', ])
def query_all_city(data):
    tunel = data['message']['chat']['id']
    result_text = 'Список городов'
    reply_markup = settings_user.template_city()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.message_handler(commands=['Перевозчик', ])
def query_all_delivery(data):
    tunel = data['message']['chat']['id']
    result_text = 'Перевозчики'
    reply_markup = settings_user.template_delivery()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}
    return message, bot.api_url


@dp.message_handler(commands=['Регион', ])
def query_all_region(data):
    tunel = data['message']['chat']['id']
    result_text = 'Echo'
    reply_markup = settings_user.template_region_all()
    message = {'chat_id': tunel, 'text': result_text, 'reply_markup': reply_markup}

    return message, bot.api_url


@dp.callback_handler(commands=['city', ])
def test2(data):

    callback_hello_ok(data, "ok!")

    tunnel = data['callback_query']['message']['chat']['id']
    result_text = 'Список городов'
    reply_markup = settings_user.template_city()
    message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
    curl = bot.api_url
    return message, curl


@dp.callback_handler(commands=['shop', ])
def test_list(data):

    callback_hello_ok(data, 'ok!')

    tunnel = data['callback_query']['message']['chat']['id']
    result_text = 'Echo'
    reply_markup = settings_user.template_shops()
    res = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}

    curl = bot.api_url
    return res, curl


def dummy_message(data):
    """ Заглушка для message """
    text = data['message'].get('text')
    logging.info(settings_user.HANDLER_USER_ADR)
    result_text = f"Функция [{text}] в разработке."
    res = {'chat_id': data['message']['chat']['id'], 'text': result_text}
    return res,  bot.api_url


def dummy_callback(data):
    """ Заглушка для callback_query """

    planner.start_proc()  # Run planner in different process
    logging.info("I am!")

    text = data['callback_query']['data']
    result_text = f"Функция [ {text} ] в разработке."
    res = {"callback_query_id": data['callback_query']['id'],
           "text": result_text, "cache_time": 3}
    return res, bot.api_answer


def handler_response_ok(resp):
    """ Обработчик успешного ответа от сервера """
    data = resp.json()
    if isinstance(data, dict):
        if data['result'] == True:
            pass
        elif id_sms := data['result'].get('message_id'):
            # logging.info(data)
            chat_id = data['result']['chat']['id']
            dredis.put_redis_last_messge_bot(chat_id, id_sms)  # Save to Redis


@bottle.route('/api/v1/echo', method='POST')
def do_echo():
    """ Main """

    message = {}
    curl = None

    # get or set settings users regions to variable DICT_INIT
    dredis.variable_init()

    data = request.json
    logging.info(data)

    if bot.last_id < data['update_id']:
        # Отсекаем старые сообщения если ид меньше текущего
        bot.last_id = data['update_id']

        if data.get('callback_query'):
            # curl = bot.api_answer
            if commands := data['callback_query'].get('data'):
                if exec_func := dp.pull_callback_commands.get(commands):
                    message, curl = exec_func(data)
                else:
                    message, curl = dummy_callback(data)

        if data.get('message'):
            # curl = bot.api_url
            if commands := data['message'].get('text'):

                dredis.put_redis_message_user(data)

                if exec_func := dp.pull_message_commands.get(commands):
                    logging.info(commands)
                    message, curl = exec_func(data)
                else:
                    message, curl = dummy_message(data)

        if message and curl:
            # logging.info(message)
            # logging.info(curl)
            try:
                r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
                assert r.status_code == 200

                #handler_response_ok(r, redisClient)  # Обработчик ответа

            except Exception as ex:
                logging.info(r)
                logging.error('Error' + str(ex))

    # logging.info('old_message')
    # logging.info(data)


