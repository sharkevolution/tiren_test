# def callback_handler(commands):
#     def decorator(fn):
#         for b in commands:
#             pull_callback_commands = fn
#
#         def decorated2(*args, **kwargs):
#             return fn(*args, **kwargs)
#
#         decorated2.__name__ = fn.__name__
#         return decorated2
#
#     return decorator
#
#
# @callback_handler("new")
# def f(data):
#     print(data)
#
# data = {'key': 0}
#
#
# f(data)


# import msgpack
#
# d = {'last': 1}
# g  = msgpack.packb(d)
#
# f = msgpack.unpackb(g)
# print(f)


import emoji
r = emoji.emojize(':two_o\u2019clock:')

