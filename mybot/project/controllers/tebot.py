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


class Bot:
    """ Bot token """

    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.api_answer = f'https://api.telegram.org/bot{self.token}/answerCallbackQuery'
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}


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


API_TOKEN = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['/start', ])
def start(data):
    reply_markup = {"keyboard": [[{"text": "Город"}], [{"text": "Регион"}], ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    result_text = 'Echo'
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text,
        'reply_markup': reply_markup,
    }

    curl = bot.api_url

    return message, curl


@dp.message_handler(commands=['Город', ])
def test1(data):
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
        'reply_markup': reply_markup,
    }

    curl = bot.api_url

    return message, curl


@dp.message_handler(commands=['Перевозчик', ])
def test2(data):
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

    curl = bot.api_url

    return message, curl


@dp.message_handler(commands=['Регион', ])
def test3(data):
    # ---
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

    curl = bot.api_url
    return message, curl


@dp.callback_handler(commands=['city', ])
def test2(data):
    reply_markup = {"keyboard": [[{"text": "Звездец"}],
                                 [{"text": "Капец"}],
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    result_text = 'Echo'
    message = {
        'chat_id': data['callback_query']['id'],
        'text': result_text,
        'reply_markup': reply_markup,
    }

    curl = bot.api_url
    return message, curl



def dummy_message(data):
    text = str(data['message']['text'])
    result_text = f"Функция [{text}] в разработке."

    res = {
        'chat_id': data['message']['chat']['id'],
        'text': result_text}

    curl = bot.api_url
    return res, curl


def dummy_callback(data):
    text = str(data['callback_query']['data'])
    result_text = f"Функция [ {text} ] в разработке."

    res = {"callback_query_id": data['callback_query']['id'],
               "text": result_text,
               "cache_time": 3}
    curl = bot.api_answer
    return res, curl


@bottle.route('/api/v1/echo', method='POST')
def do_echo_two():
    """ Main """
    redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    # try:
    data = request.json
    message = {}
    curl = None

    if data.get('callback_query'):
        # curl = bot.api_answer
        commands = data['callback_query']['data']
        if exec_func := dp.pull_callback_commands.get(commands):
            message, curl = exec_func(data)
        else:
            message, curl = dummy_callback(data)

    if data.get('message'):
        # curl = bot.api_url
        commands = data['message']['text']
        if exec_func := dp.pull_message_commands.get(commands):
            message, curl = exec_func(data)
        else:
            message, curl = dummy_message(data)

    logging.info(message)
    r = requests.post(curl, data=json.dumps(message), headers=bot.headers)
    assert r.status_code == 200

    # except Exception as ex:
    #     logging.info('Error' + str(ex))


    # if call.message:
    #     if call.data == "test":
    #         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
    #         bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пыщь!")