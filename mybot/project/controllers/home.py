# -*- coding: UTF-8 -*-
import bottle
from bottle import view, request, redirect
from mybot.project.controllers import mail

import json
import requests
import logging


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


@bottle.route('/api/v1/echo', method='POST')
def do_echo():
    bottoken = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
    api_url = 'https://api.telegram.org/bot{0}/sendMessage'.format(bottoken)

    reply_markup = {
        "keyboard": [[{"text": "1"}], [{"text": "2"}]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }


    try:

        data = request.json
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
