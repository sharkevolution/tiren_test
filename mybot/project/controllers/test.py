# def dynamic_range_adr(self):
#     list_adr = []
#     if ch := self.users.get(self.last_chat):
#         list_adr = ch.adr
#     return list_adr
#
#
# def dynamic_range_delivery(self):
#     list_delivery = []
#     if ch := self.users.get(self.last_chat):
#         list_delivery = ch.delivery
#     return list_delivery

# @dp.message_handler(commands=['Город', ])
# def query_all_city(data):
#     tunnel = data['message']['chat']['id']
#     result_text = 'Список городов'
#     reply_markup = settings_user.template_city()
#     message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
#     return message, bot.api_url


# @dp.message_handler(commands=['Перевозчик', ])
# def query_all_delivery(data):
#     tunnel = data['message']['chat']['id']
#     result_text = 'Перевозчики'
#     reply_markup = settings_user.template_delivery()
#     message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
#     return message, bot.api_url


# @dp.message_handler(commands=['Регион', ])
# def query_all_region(data):
#     tunnel = data['message']['chat']['id']
#     result_text = 'Echo'
#     reply_markup = settings_user.template_region_all()
#     message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
#     return message, bot.api_url


# @dp.callback_handler(commands=['city', ])
# def test2(data):
#     callback_hello_ok(data, "ok!")
#
#     tunnel = data['callback_query']['message']['chat']['id']
#     result_text = 'Список городов'
#     reply_markup = settings_user.template_city()
#     message = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
#     curl = bot.api_url
#     return message, curl


# @dp.callback_handler(commands=['shop', ])
# def test_list(data):
#     callback_hello_ok(data, 'ok!')
#
#     tunnel = data['callback_query']['message']['chat']['id']
#     result_text = 'Echo'
#     reply_markup = settings_user.template_shops()
#     res = {'chat_id': tunnel, 'text': result_text, 'reply_markup': reply_markup}
#
#     curl = bot.api_url
#     return res, curl




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


# import emoji
# r = emoji.emojize(':satellite:')
# print(r)

# def hhhh(my):
#     print(type(my))
#
#
# class open():
#
#     def __init__(self):
#         self.g = [1, 23]
#
#
# f = open()
# hhhh(f.g)


# d = '12:5'
# f = d.split(':')
# print(f)