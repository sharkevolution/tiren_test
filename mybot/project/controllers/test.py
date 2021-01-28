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

# import copy
#
# number_key = {'ent_one': 1, 'ent_two': 2, 'ent_three': 3, 'ent_four': 4,
#               'ent_five': 5, 'ent_six': 6, 'ent_seven': 7, 'ent_eight': 8,
#               'ent_nine': 9, 'ent_zero': 0, 'ent_colon': ':'}
#
# valid_range = {'01': 1, '02': 1, '03': 1, '04': 1, '05': 1, '06': 1, '07': 1,
#                '08': 1, '09': 1, '10': 1, '11': 1, '12': 1, '13': 1, '14': 1,
#                '15': 1, '16': 1, '17': 1, '18': 1, '19': 1, '20': 1, '21': 1,
#                '22': 1, '23': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
#                '7': 1, '8': 1, '9': 9, '0': 0}
#
#
# def my(ord, comb):
#
#     tmp_list = copy.deepcopy(comb)
#     # if str(number_key[ord]) in valid_range:
#
#     if ':' in tmp_list:
#         ind = tmp_list.index(':')
#         left_side = tmp_list[:ind]
#         right_side = tmp_list[ind + 1:]
#
#         if right_side:
#             if len(right_side) == 1:
#                 if str(number_key[ord]) in '0123456789':
#                     right_side.append(str(number_key[ord]))
#         else:
#             if str(number_key[ord]) in '012345':
#                 right_side.append(str(number_key[ord]))
#
#         tmp_list = left_side + [':'] + right_side
#         #print(tmp_list)
#
#     else:
#         left_side = []
#         if len(tmp_list) == 1:
#             if int(tmp_list[0]) == 2:
#                 if str(number_key[ord]) in '0123:':
#                     left_side.append(str(number_key[ord]))
#                     tmp_list += left_side
#             else:
#                 if tmp_list[0] in '3456789':
#                     pass
#                 else:
#                     left_side.append(str(number_key[ord]))
#                     tmp_list += left_side
#             if not ':' == str(number_key[ord]):
#                 # left_side.append(':')
#                 tmp_list += ':'
#
#             # tmp_list += left_side
#             if len(tmp_list) == 2:
#                 tmp_list.insert(0, '0')
#                 new_comb = copy.deepcopy(tmp_list)
#                 tmp_list = my(ord, new_comb)
#
#         elif len(tmp_list) == 2:
#             left_side.append(':')
#             tmp_list += left_side
#         else:
#             if str(number_key[ord]) in '0123456789':
#                 left_side.append(str(number_key[ord]))
#             tmp_list += left_side
#         #print(tmp_list)
#
#     comb = copy.deepcopy(tmp_list)
#
#     return comb
#
# #y = my('ent_three', [])
#
# y1 = my('ent_two', ['1',])
# y2 = my('ent_two', y1)
# y3 = my('ent_five', y2)
#
# #print(''.join(y))
# print(y1)
# print(y2)
# print(y3)

from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

print(date_time)

