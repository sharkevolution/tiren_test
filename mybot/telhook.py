#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# https://core.telegram.org/bots/webhooks#the-verbose-version
# https://gist.github.com/subfuzion/08c5d85437d5d4f00e5
# https://andreafortuna.org/programming/how-to-build-a-simple-echo-bot-on-telegram-using-hook-io-and-python/
# https://habrahabr.ru/post/322078/
# https://tyvik.ru/posts/telegram-bot-setwebhook
# https://habrahabr.ru/post/262247/
# https://groosha.gitbooks.io/telegram-bot-lessons/content/chapter4.html



# def app(environ, start_response):
#     bottoken = 'YOUR_BOT_TOKEN'
#     baseURL = 'https://api.telegram.org/bot'
#
#     data = json.loads(json.dumps(Hook['params']))
#     chat_id = data['message']['chat']['id']
#     message = data['message']['text']
#     data = {"chat_id": chat_id, "text": message}
#     sendURL = baseURL + bottoken + "/sendMessage"
#     headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#     requests.post(sendURL, data=json.dumps(data), headers=headers, verify=False)
#
#     start_response('200 OK', [('content-type', 'text/plain')])
#     return '\n'


import json
import requests

bottoken = '528159377:AAEI3Y3zTYv18e2qBp_nXBBMxLZU1uUhPHg'
baseURL = 'https://api.telegram.org/bot{0}/setWebhook'.format(bottoken)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {"url": ""}

r = requests.get(baseURL, headers=headers, data=json.dumps(data))
r.text


