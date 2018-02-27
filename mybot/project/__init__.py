# -*- coding: UTF-8 -*-

import os
import bottle
from bottle import TEMPLATE_PATH
from beaker.middleware import SessionMiddleware

from mybot import config

# Add view paths to the Bottle template path
TEMPLATE_SUB_PATHS = next(os.walk(config.BASE_TEMPLATE_PATH))[1]
TEMPLATE_PATH.append(config.BASE_TEMPLATE_PATH)

for templatePath in TEMPLATE_SUB_PATHS:
    TEMPLATE_PATH.append(os.path.join(config.BASE_TEMPLATE_PATH, templatePath))


session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 30,  # Время в сек через которое закончится текущая сессия
    'session.data_dir': './data',  # Директория для хранения сесии
    'session.auto': True
}

# app = Bottle()
app = SessionMiddleware(bottle.app(), session_opts)

from .controllers import *

# if config.DEBUG:
#     print("ROOT_PATH: %s" % config.ROOT_PATH)
#     print("Template Paths:")
#
#     for it in bottle.TEMPLATE_PATH:
#         print("   %s" % it)

