# -*- coding: UTF-8 -*-
#!/usr/bin/python

import os
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

import os
import cherrypy
import wsgigzip

from mybot.project import app

host = "0.0.0.0"
port = int(os.environ.get("PORT", 5000))
def_app = wsgigzip.GzipMiddleware(app)

# --------------------------------------------------------------
# cherrypy.config.update({'server.socket_host': host,
#                         'server.socket_port': port})
# cherrypy.tree.graft(def_app)
# cherrypy.engine.start()
# cherrypy.engine.block()
#----------------------------------------------------------------

# server = WSGIServer((host, port), def_app, handler_class=WebSocketHandler)
# server.serve_forever()

# https://gist.github.com/dusual/9838932





# from gevent import monkey
# monkey.patch_all()
# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler
#
# import os
# import cherrypy
# import wsgigzip
#
# from lime.project import app
#
# host = "0.0.0.0"
# port = int(os.environ.get("PORT", 5000))
# def_app = wsgigzip.GzipMiddleware(app)
# # app = wsgigzip.GzipMiddleware(bottle.default_app())
#
# # --------------------------------------------------------------
# # cherrypy.config.update({'server.socket_host': host,
# #                         'server.socket_port': port})
# # cherrypy.tree.graft(def_app)
# # cherrypy.engine.start()
# # cherrypy.engine.block()
# #----------------------------------------------------------------

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

server = WSGIServer((host, port), def_app, handler_class=WebSocketHandler)
server.serve_forever()