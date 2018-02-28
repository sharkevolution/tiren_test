# -*- coding: UTF-8 -*-
import bottle
from bottle import view, request, redirect
from mybot.project.controllers import mail

import json
import requests


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


@bottle.route('/api/v1/echo')
def do_echo(res):
    bottoken = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
    baseURL = 'https://api.telegram.org/bot{0}/setWebhook'.format(bottoken)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    api_url = 'https://api.telegram.org/bot{0}/sendMessage'.format(bottoken)

    data = res.json()
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': data['message']['text']
    }

    try:
        r = requests.post(api_url, data=json.dumps(message), headers=headers)

        assert r.status == 200

    except:
        return '500'
    return '200'
