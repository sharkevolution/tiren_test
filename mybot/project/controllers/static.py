
import os
import bottle
from bottle import static_file

from mybot.project import config


@bottle.route('/resources/<action>/<filepath:path>')
def server_static(action, filepath):
    root = os.path.join(config.RESOURCES_PATH, action)
    return static_file(filepath, root=root)


# @bottle.route('/:path#(images|css|js|fonts)\/.+#')
# def server_static(path):
#     return static_file(path, root='project/
