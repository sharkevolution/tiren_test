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
import types

import emoji
import redis

from mybot.project.controllers import planner


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

dict_region = {'Днепр': {'Днепр': ['aaa']},
               'Львов': {'Львов': 'ddd'},
               'Одесса': {'Николаев': 'xxx',
                          'Херсон': 'fff'},
               'Харьков': [],
               'Николаев': [],
               'Тернополь': [],
               'Запорожье': [],
               'Чернигов': []}

# ej_ukraine = emoji.emojize(':Ukraine:')
# ej_city = emoji.emojize(':cityscape:')
# ej_delivery = emoji.emojize(':delivery_truck:')
# ej_shop = emoji.emojize(':shopping_cart:')

start_reply = [
    [{"text": f"Выбрать регионы {emoji.emojize(':Ukraine:')}", "callback_data": "region"},
     {"text": f"Выбрать города {emoji.emojize(':cityscape:')}", "callback_data": "city"}],
    [{"text": f"Заполнить время прибытия {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
    [{"text": f"Мои сообщения {emoji.emojize(':shopping_cart:')}", "callback_data": "delivery"}, ],
    [{"text": f"Мои регионы {emoji.emojize(':shopping_cart:')}", "callback_data": "shop"}, ],
    [{"text": f"Мои города {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
    [{"text": f"Удалить время прибытия {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
    [{"text": f"Удалить регионы {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
    [{"text": f"Удалить города {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
]


@dp.callback_handler(commands=['enter_one', 'enter_two', 'enter_three',
                               'enter_four', 'enter_five', 'enter_six', 'enter_seven',
                               'enter_eight', 'enter_nine', 'enter_zero'])
def enter(data):

    # Обязательный ответ Callback *********************************
    result_text = 'ok!'
    message = {"callback_query_id": data['callback_query']['id'],
               "text": result_text,
               "cache_time": 3}

    curl = bot.api_answer
    r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    # Редактируем сообщение
    bot.user_combination.append('1')
    my_test = ''.join(bot.user_combination)

    base_keys = get_redis_message(data)
    if base_keys:
        last_message_id = base_keys['sms_id_last_bot']

    curl = bot.api_edit_message
    message = {'chat_id': data['callback_query']['message']['chat']['id'],
               'message_id': last_message_id,
               'text': my_test}


    logging.info('EDIT Message')
    logging.info(bot.last_message_id)
    return message, curl


@dp.message_handler(commands=['/idc', ])
def bind_bot(data):

    message = {
        'chat_id': data['message']['chat']['id'],
        'text': data['message']['chat']['id'],
    }
    return message, bot.api_url


@dp.message_handler(commands=['/bc', ])
def keboard_bot(data):

    ej_ok = emoji.emojize(':OK_button:')

    reply_markup = {"inline_keyboard": [[
        {"text": f"{emoji.emojize(' 1 ')}", "callback_data": "enter_one"},
        {"text": f"{emoji.emojize(' 2 ')}", "callback_data": "enter_two"},
        {"text": f"{emoji.emojize(' 3 ')}", "callback_data": "enter_three"}],

        [{"text": f"{emoji.emojize(' 4 ')}", "callback_data": "enter_four"},
        {"text": f"{emoji.emojize(' 5 ')}", "callback_data": "enter_five"},
        {"text": f"{emoji.emojize(' 6 ')}", "callback_data": "enter_six"}],

        [{"text": f"{emoji.emojize(' 7 ')}", "callback_data": "enter_seven"},
         {"text": f"{emoji.emojize(' 8 ')}", "callback_data": "enter_eight"},
         {"text": f"{emoji.emojize(' 9 ')}", "callback_data": "enter_nine"}],

        [{"text": f"{emoji.emojize(' 0 ')}", "callback_data": "enter_zero"},
         {"text": f"{ej_ok}", "callback_data": "enter_ok"}]
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False}

    result_text = 'Engineer Mode Ti'
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup,
    }

    r = requests.post(bot.api_url, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    # Input pass
    bot.user_combination = []
    result_text = "Input key: "
    message = {'chat_id': data['message']['chat']['id'], 'text': result_text}

    return message, bot.api_url


@dp.message_handler(commands=['/start', ])
def start_bot(data):
    reply_markup = {"inline_keyboard": start_reply,
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    result_text = 'Echo'
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup,
    }

    return message, bot.api_url


@dp.message_handler(commands=['Город', ])
def query_all_city(data):
    reply_markup = {"keyboard": [[{"text": "Днепр"}],
                                 [{"text": "Львов"}],
                                 [{"text": "Одесса"}],
                                 [{"text": "Херсон"}],
                                 [{"text": "Николаев"}],
                                 [{"text": "Регион"}],
                                 [{"text": "Перевозчик"}],
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    result_text = 'Echo'
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup, }

    return message, bot.api_url


@dp.message_handler(commands=['Перевозчик', ])
def query_all_delivery(data):
    reply_markup = {"keyboard": [[{"text": "ВИП"}],
                                 [{"text": "Координатор"}],
                                 [{"text": "Космос"}],
                                 [{"text": "Курьер"}],
                                 [{"text": "Регион"}],
                                 [{"text": "Город"}]
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    result_text = 'Echo'
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup,
    }

    return message, bot.api_url


@dp.message_handler(commands=['Регион', ])
def query_all_region(data):
    ej_ukraine = emoji.emojize(':Ukraine:')
    ej_city = emoji.emojize(':cityscape:')
    ej_delivery = emoji.emojize(':delivery_truck:')
    ej_shop = emoji.emojize(':shopping_cart:')

    reply_markup = {"inline_keyboard": [[
        {"text": f"Регион {ej_ukraine}", "callback_data": "region"},
        {"text": f"Город {ej_city}", "callback_data": "city"}],
        [{"text": f"Магазин {ej_shop}", "callback_data": "shop"}, ],
        [{"text": f"Перевозчик {ej_delivery}", "callback_data": "delivery"}, ]
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False}

    result_text = 'Echo'
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup,
    }

    return message, bot.api_url


@dp.callback_handler(commands=['city', ])
def test2(data):
    result_text = 'ok!'
    message = {"callback_query_id": data['callback_query']['id'],
               "text": result_text,
               "cache_time": 3}

    # Обязательный ответ Callback
    curl = bot.api_answer
    r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    # Можно отправлять запросы после
    reply_markup = {"keyboard": [[{"text": "Звездец"}],
                                 [{"text": "Трындец"}],
                                 [{"text": "Перевозчик"}],
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}
    result_text = 'Echo'
    res = {
        'chat_id': data['callback_query']['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup, }

    curl = bot.api_url
    return res, curl


@dp.callback_handler(commands=['shop', ])
def test_list(data):
    result_text = 'ok!'
    message = {"callback_query_id": data['callback_query']['id'],
               "text": result_text,
               "cache_time": 3}

    # Обязательный ответ Callback
    curl = bot.api_answer
    r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    # ---------------------------------
    logging.info(bot.message_id_list)

    # Можно отправлять запросы после
    reply_markup = {"keyboard": [[{"text": "Выполнено"}],
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}
    result_text = 'Echo'
    res = {
        'chat_id': data['callback_query']['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup, }

    curl = bot.api_url
    return res, curl


def dummy_message(data):
    """ Заглушка для message """

    text = str(data['message'].get('text'))
    result_text = f"Функция [{text}] в разработке."
    res = {'chat_id': data['message']['chat']['id'], 'text': result_text}
    return res,  bot.api_url


def dummy_callback(data):
    """ Заглушка для callback_query """

    planner.start_proc()  # Run planner in different process

    text = str(data['callback_query']['data'])
    result_text = f"Функция [ {text} ] в разработке."
    res = {"callback_query_id": data['callback_query']['id'],
           "text": result_text, "cache_time": 3}
    return res, bot.api_answer


def get_redis_message(data):
    """ Add to Redis last messge Bot """

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    chat_id = data['message']['chat']['id']

    h = redisClient.hget(chat_id)
    logging.info(h)

    return h


def put_redis_message_user(data, redisClient):
    """ Add to Redis last messge User """

    chat_id = data['message']['chat']['id']
    sms_id_last_user = data['message']['from']['id']

    base_keys = get_redis_message(data)
    if base_keys:
        base_keys['sms_id_last_user'] = sms_id_last_user
    else:
        base_keys = {'sms_id_last_user': sms_id_last_user}

    redisClient.hmset(chat_id, base_keys)


def put_redis_message_bot(data, redisClient):
    """ Add to Redis last messge Bot """

    chat_id = data['message']['chat']['id']
    sms_id_last_bot = data['message']['from']['id']

    base_keys = get_redis_message(data)
    if base_keys:
        base_keys['sms_id_last_bot'] = sms_id_last_bot
    else:
        base_keys = {'sms_id_last_bot': sms_id_last_bot}

    redisClient.hmset(chat_id, base_keys)


def handler_response_ok(resp, redisClient):
    """ Обработчик успешного ответа от сервера """

    data = resp.json()

    if isinstance(data, dict):
        if id_sms := data['result'].get('message_id'):
            bot.last_message_id = id_sms

            put_redis_message_bot(data, redisClient)  # Save to Redis

    logging.info(bot.last_message_id)
    logging.info(data)


@bottle.route('/api/v1/echo', method='POST')
def do_echo():
    """ Main """

    message = {}
    curl = None

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))

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

                put_redis_message_user(data, redisClient)

                if exec_func := dp.pull_message_commands.get(commands):
                    logging.info(commands)
                    message, curl = exec_func(data)
                else:
                    message, curl = dummy_message(data)

        if message and curl:
            #logging.info(message)
            #logging.info(curl)
            try:
                r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
                assert r.status_code == 200

                handler_response_ok(r, redisClient)  # Обработчик ответа

            except Exception as ex:
                logging.info(r)
                logging.error('Error' + str(ex))

    logging.info('old_message')
    logging.info(data)


