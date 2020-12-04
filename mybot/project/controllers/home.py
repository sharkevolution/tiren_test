# -*- coding: UTF-8 -*-
import bottle
from bottle import view, request, redirect
from mybot.project.controllers import mail

import os
import json
import requests
import logging

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

def dispatch():
    def actual_decorator(func):
        def wrapper(*args, **kwargs):

            return_value = func(*args, **kwargs)
            logging.info('ok'*10)
            return return_value
        return wrapper
    return actual_decorator


@bottle.route('/api/v1/echo', method='POST')
@dispatch()
def do_echo(data):

    r = redis.from_url(os.environ.get("REDIS_URL"))
    logging.info(f'Redis {r}')

    bottoken = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
    api_url = 'https://api.telegram.org/bot{0}/sendMessage'.format(bottoken)

    # Добавляем клавиатуру
    reply_markup = {"keyboard": [[{"text": "Регион"}], [{"text": "2"}], [{"text": "3"}]],
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    try:
        data = request.json

        logging.info(str(data))

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        message = {
            'chat_id': data['message']['chat']['id'],
            'text': "".join(['эхо', "_", str(data['message']['text'])]),
            'reply_markup': reply_markup
        }

        r = requests.post(api_url, data=json.dumps(message), headers=headers)

        assert r.status_code == 200

    except Exception as ex:
        logging.info(str(ex))
        return '500'
    return '200'



# 'message': {'message_id': 425,
#             'from': {'id': 471125560, 'is_bot': False, 'first_name': 'Kolya', 'last_name': 'Sitala', 'language_code': 'ru'},
#             'chat': {'id': 471125560, 'first_name': 'Kolya', 'last_name': 'Sitala', 'type': 'private'},
#             'date': 1607086983,
#             'text': '1'}



