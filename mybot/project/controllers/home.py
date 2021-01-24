# -*- coding: UTF-8 -*-
import bottle
from bottle import view, request, redirect
from mybot.project.controllers import mail

# https://unicode.org/emoji/charts/full-emoji-list.html#1f600
# https://apps.timwhitlock.info/emoji/tables/unicode
# https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py


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
