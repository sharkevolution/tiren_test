# -*- coding: UTF-8 -*-
import bottle
from bottle import view, request, redirect
from mybot.project.controllers import mail

import os
import json
import requests
import logging
import types

import redis


# @bottle.route('/api/v1/echo', method='POST')
# @benchmark(mt=1)
# def do_echo():
#
#     bottoken = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
#     api_url = 'https://api.telegram.org/bot{0}/sendMessage'.format(bottoken)
#
#     # Добавляем клавиатуру
#     reply_markup = {"keyboard": [[{"text": "1"}], [{"text": "2"}], [{"text": "3"}]],
#                     "resize_keyboard": True,
#                     "one_time_keyboard": False}
#
#     try:
#         data = request.json
#
#         logging.info(str(data))
#
#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#         message = {
#             'chat_id': data['message']['chat']['id'],
#             'text': "".join(['эхо', "_", str(data['message']['text'])]),
#             'reply_markup': reply_markup
#         }
#
#         r = requests.post(api_url, data=json.dumps(message), headers=headers)
#
#         assert r.status_code == 200
#
#     except Exception as ex:
#         logging.info(str(ex))
#         return '500'
#     return '200'


@bottle.route('/')
@view('index')
def index():
    return dict(csf="resources/css/styles.css")


@bottle.route('/send', method='POST')
def do_admin():
    user_name = request.forms.get('name')
    user_text = request.forms.get('text')

    # mail.send_mail('nsitala@gmail.com', 'nsitala@gmail.com', user_name, user_text)
    mail.send_sms(user_name, user_text)
    redirect('/')


# InlineKeyboardButton

# def dispatch():
#     def actual_decorator(func):
#         def wrapper(*args, **kwargs):
#
#             return_value = func(*args, **kwargs)
#             logging.info('ok'*10)
#             return return_value
#         return wrapper
#     return actual_decorator


# @bottle.route('/api/v1/echo', method='POST')
# @dispatch()
# def do_echo():
#
#     redisClient = redis.from_url(os.environ.get("REDIS_URL"))
#
#     hashName = "Authors"
#     redisClient.hmset(hashName, {1: "The C Programming Language",
#                                  2: "The UNIX Programming Environment"})
#
#     logging.info(redisClient.hgetall(hashName))
#
#     bottoken = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
#     api_url = 'https://api.telegram.org/bot{0}/sendMessage'.format(bottoken)
#
#     # Добавляем клавиатуру
#     reply_markup = {"keyboard": [[{"text": "Регион"}], [{"text": "2"}], [{"text": "3"}]],
#                     "resize_keyboard": True,
#                     "one_time_keyboard": False}
#
#     try:
#         data = request.json
#
#         logging.info(str(data))
#
#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#         message = {
#             'chat_id': data['message']['chat']['id'],
#             'text': "".join(['эхо', "_", str(data['message']['text'])]),
#             'reply_markup': reply_markup
#         }
#
#         r = requests.post(api_url, data=json.dumps(message), headers=headers)
#
#         assert r.status_code == 200
#
#     except Exception as ex:
#         logging.info(str(ex))
#         return '500'
#     return '200'


# ******************************************************************************
class Bot:
    """
        Bot token
    """

    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.api_answer = f'https://api.telegram.org/bot{self.token}/answerCallbackQuery'
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}


class Dispatcher:
    """
        handler messages command
    """

    def __init__(self, bot):
        self.bot = bot
        self.commands = None
        self.pull = {}

    def message_handler(self, commands):
        def decorator(fn):
            for b in commands:
                self.pull[b] = fn

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
def start(*args, **kwargs):
    reply_markup = {"keyboard": [[{"text": "Город"}], [{"text": "Регион"}], ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    return reply_markup


@dp.message_handler(commands=['Город', ])
def test1(*args, **kwargs):
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

    return reply_markup


@dp.message_handler(commands=['Перевозчик', ])
def test2(*args, **kwargs):
    reply_markup = {"keyboard": [[{"text": "ВИП"}],
                                 [{"text": "Координатор"}],
                                 [{"text": "Космос"}],
                                 [{"text": "Курьер"}],
                                 [{"text": "Регион"}],
                                 [{"text": "Город"}]
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    return reply_markup


@dp.message_handler(commands=['Регион', ])
def test3(*args, **kwargs):

    reply_markup = {"inline_keyboard": [[
         {"text": "A", "callback_data": "Город"},
         {"text": "B", "callback_data": "Перевозчик"}]],
         "resize_keyboard": True,
         "one_time_keyboard": False}

    # reply_markup = {"keyboard": [[{"text": "Днепропетровский"}],
    #                              [{"text": "Запорожский"}],
    #                              [{"text": "Львововский"}],
    #                              [{"text": "Одессский"}],
    #                              [{"text": "Город"}],
    #                              [{"text": "Перевозчик"}],
    #                              ],
    #                 "resize_keyboard": True,
    #                 "one_time_keyboard": False}

    return reply_markup


@bottle.route('/api/v1/echo', method='POST')
def do_echo_two():
    """ Main """

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    # try:
    data = request.json
    message = {}

    if data.get('callback_query'):
        logging.info(str(data.get('callback_query')))
        commands = data['callback_query']['data']
        exec_func = dp.pull.get(commands)
        if exec_func:
            new_reaply_board = exec_func(commands)
            logging.info(str(new_reaply_board))

        logging.info(data['callback_query']['data'])

        # query.message.chat_id
        result_text = f"Функция [ callback_query ] в разработке."

        message = {"callback_query_id": data['callback_query']['id'],
                   "text": result_text,
                   "show_alert": False,
                   "url": "http://ya.ru",
                   "cache_time": 3
                   }

        try:
            r = requests.post(bot.api_answer, data=json.dumps(message), headers=bot.headers)
            logging.info(r)
            assert r.status_code == 200

        except Exception as ex:
            logging.info('Error' + str(ex))
            return '500'

        # message = {
        #     'chat_id': data['callback_query']['message']['chat']['id'],
        #     'text': result_text,
        # }

    if data.get('message'):

        from_id = data['message']['from']['id']
        first_name = data['message']['from']['first_name']
        last_name = data['message']['from']['first_name']

        redisClient.hmset(from_id, {'first_name': first_name,
                                    'last_name': last_name})

        commands = data['message']['text']
        exec_func = dp.pull.get(commands)
        if exec_func:
            new_reaply_board = exec_func(commands)
            logging.info(str(new_reaply_board))

        # Check function
        result_text = ''
        if type(exec_func) is types.FunctionType:
            txt = data['message']['text']
            result_text = "".join(['эхо', "_", txt])

            message = {
                'chat_id': data['message']['chat']['id'],
                'text': result_text,
                'reply_markup': new_reaply_board
            }

        else:
            txt = str(data['message']['text'])
            result_text = f"Функция [{txt}] в разработке."

            message = {
                'chat_id': data['message']['chat']['id'],
                'text': result_text,
            }

        r = requests.post(bot.api_url, data=json.dumps(message), headers=bot.headers)
        assert r.status_code == 200

    # except Exception as ex:
    #     logging.info('Error' + str(ex))
    #     return '500'
    # return '200'
