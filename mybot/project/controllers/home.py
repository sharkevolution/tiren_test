# -*- coding: UTF-8 -*-
import bottle
from bottle import view, request, redirect
from mybot.project.controllers import mail


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
def do_echo():
    return 'ok'
