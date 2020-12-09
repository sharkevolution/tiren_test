# -*- coding: UTF-8 -*-

# https://unicode.org/emoji/charts/full-emoji-list.html#1f600
# https://apps.timwhitlock.info/emoji/tables/unicode
# https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py


import bottle
from bottle import view, request, redirect

import os
import json
import requests
import logging
# import types

import emoji
import redis


class User:
    def __init__(self):
        self.messages_id = []
        self.first_name = None
        self.last_name = None

    def get_redis(self):
        pass


class Bot:
    """ Bot token """

    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.api_answer = f'https://api.telegram.org/bot{self.token}/answerCallbackQuery'
        self.api_edit_message = f'https://api.telegram.org/bot{self.token}/editMessageText'
        self.api_get_updates = f'https://api.telegram.org/bot{self.token}/getUpdates'

        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
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

ej_ukraine = emoji.emojize(':Ukraine:')
ej_city = emoji.emojize(':cityscape:')
ej_delivery = emoji.emojize(':delivery_truck:')
ej_shop = emoji.emojize(':shopping_cart:')

start_reply = [
    [{"text": f"Выбрать регионы {emoji.emojize(':Ukraine:')}", "callback_data": "region"},
     {"text": f"Выбрать города {emoji.emojize(':cityscape:')}", "callback_data": "city"}],
    [{"text": f"Заполнить время прибытия {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
    [{"text": f"Мои сообщения {ej_delivery}", "callback_data": "delivery"}, ],
    [{"text": f"Мои регионы {emoji.emojize(':shopping_cart:')}", "callback_data": "shop"}, ],
    [{"text": f"Мои города {ej_delivery}", "callback_data": "delivery"}, ],
    [{"text": f"Удалить время прибытия {ej_delivery}", "callback_data": "delivery"}, ],
    [{"text": f"Удалить регионы {ej_delivery}", "callback_data": "delivery"}, ],
    [{"text": f"Удалить города {ej_delivery}", "callback_data": "delivery"}, ],
]


@dp.message_handler(commands=['/idc', ])
def bind_bot(data):

    message = {
        'chat_id': data['message']['chat']['id'],
        'text': data['message']['chat']['id'],
    }
    return message, bot.api_url



@dp.message_handler(commands=['/bc', ])
def bind_bot(data):

    ej_ok = emoji.emojize(':OK_button:')

    reply_markup = {"inline_keyboard": [[
        {"text": f"{emoji.emojize(':keycap_digit_one:')}", "callback_data": "enter_one"},
        {"text": f"{emoji.emojize(':keycap_digit_two:')}", "callback_data": "enter_two"},
        {"text": f"{emoji.emojize(':keycap_digit_three:')}", "callback_data": "enter_three"}],

        [{"text": f"{emoji.emojize(':keycap_digit_four:')}", "callback_data": "enter_four"},
        {"text": f"{emoji.emojize(':keycap_digit_five:')}", "callback_data": "enter_five"},
        {"text": f"{emoji.emojize(':keycap_digit_six:')}", "callback_data": "enter_six"}],

        [{"text": f"{emoji.emojize(':keycap_digit_seven:')}", "callback_data": "enter_seven"},
         {"text": f"{emoji.emojize(':keycap_digit_eight:')}", "callback_data": "enter_eight"},
         {"text": f"{emoji.emojize(':keycap_digit_nine:')}", "callback_data": "enter_nine"}],

        [{"text": f"{emoji.emojize(':keycap_digit_zero:')}", "callback_data": "enter_zero"},
        {"text": f"{ej_ok}", "callback_data": "enter_ok"}]
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
    text = str(data['message'].get('text'))
    result_text = f"Функция [{text}] в разработке."

    res = {'chat_id': data['message']['chat']['id'], 'text': result_text}

    curl = bot.api_url
    return res, curl


def dummy_callback(data):
    text = str(data['callback_query']['data'])
    result_text = f"Функция [ {text} ] в разработке."

    res = {"callback_query_id": data['callback_query']['id'],
           "text": result_text, "cache_time": 3}
    curl = bot.api_answer
    return res, curl


@bottle.route('/api/v1/echo', method='POST')
def do_echo():
    """ Main """
    redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    # try:
    data = request.json

    if data.get('callback_query'):
        # curl = bot.api_answer
        if commands := data['callback_query']['data']:
            if exec_func := dp.pull_callback_commands.get(commands):
                message, curl = exec_func(data)
            else:
                message, curl = dummy_callback(data)

            logging.info(message)
            logging.info(curl)
            r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
            assert r.status_code == 200

    if data.get('message'):
        # curl = bot.api_url

        # Сохраняем ид сообщения
        bot.message_id_list.append(data['message']['message_id'])

        if commands := data['message'].get('text'):
            if exec_func := dp.pull_message_commands.get(commands):
                message, curl = exec_func(data)
            else:
                message, curl = dummy_message(data)

            logging.info(message)
            logging.info(curl)
            r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
            assert r.status_code == 200

    # except Exception as ex:
    #     logging.info('Error' + str(ex))

    # if call.message:
    #     if call.data == "test":
    #         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
    #         bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пыщь!")
