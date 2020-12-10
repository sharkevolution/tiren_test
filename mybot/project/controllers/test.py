
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



t = {'dcs': {'ff': 0}}

r = t['dcs'].get('ff')

data = {'ss': 1}

if isinstance(data, dict):
    if id_sms := data.get('ss'):
        print('ok')