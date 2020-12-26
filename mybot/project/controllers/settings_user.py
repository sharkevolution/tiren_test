import emoji
import logging


# [{"text": f"Мои перевозчики {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Удалить время прибытия {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Удалить регионы {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Удалить города {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Мои города {emoji.emojize(':shopping_cart:')}", "callback_data": "delivery"}, ],
# [{"text": f"Мои адреса {emoji.emojize(':shopping_cart:')}", "callback_data": "shop"}, ],
# [{"text": f"Настройки бота {emoji.emojize(':shopping_cart:')}", "callback_data": "shop"}, ],

# def template_region_all():
#     ej_ukraine = emoji.emojize(':Ukraine:')
#     ej_city = emoji.emojize(':cityscape:')
#     ej_delivery = emoji.emojize(':delivery_truck:')
#     ej_shop = emoji.emojize(':shopping_cart:')
#
#     reply_markup = {"inline_keyboard": [[
#         {"text": f"Регион {ej_ukraine}", "callback_data": "region"},
#         {"text": f"Город {ej_city}", "callback_data": "city"}],
#         [{"text": f"Магазин {ej_shop}", "callback_data": "shop"}, ],
#         [{"text": f"Перевозчик {ej_delivery}", "callback_data": "delivery"}, ]
#     ],
#         "resize_keyboard": True,
#         "one_time_keyboard": False}
#
#     return reply_markup


def template_engineer_mode():
    ej_ok = emoji.emojize(':OK_button:')

    reply_markup = {"inline_keyboard": [
        [
            {"text": f"{emoji.emojize(' 1 ')}", "callback_data": "ent_one"},
            {"text": f"{emoji.emojize(' 2 ')}", "callback_data": "ent_two"},
            {"text": f"{emoji.emojize(' 3 ')}", "callback_data": "ent_three"},
            {"text": f"{emoji.emojize(':rocket: Отправить')}", "callback_data": "ent_send"}
        ],

        [
            {"text": f"{emoji.emojize(' 4 ')}", "callback_data": "ent_four"},
            {"text": f"{emoji.emojize(' 5 ')}", "callback_data": "ent_five"},
            {"text": f"{emoji.emojize(' 6 ')}", "callback_data": "ent_six"},
            {"text": f"{emoji.emojize(':TOP_arrow: Главная')}", "callback_data": "ent_main"}
        ],

        [
            {"text": f"{emoji.emojize(' 7 ')}", "callback_data": "ent_seven"},
            {"text": f"{emoji.emojize(' 8 ')}", "callback_data": "ent_eight"},
            {"text": f"{emoji.emojize(' 9 ')}", "callback_data": "ent_nine"},
            {"text": f"{emoji.emojize(':spiral_notepad: Список')}", "callback_data": "ent_list"}
        ],

        [
            {"text": f"{emoji.emojize(' 0 ')}", "callback_data": "ent_zero"},
            {"text": f"{emoji.emojize(' : ')}", "callback_data": "ent_colon"},
            {"text": f"{emoji.emojize(':BACK_arrow:')}", "callback_data": "ent_backspace"},
            {"text": f"{emoji.emojize(':houses: Адреса')}", "callback_data": "ent_shops"}
        ],
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False}

    return reply_markup


def template_gear_del_address(dict_init, chat_user):
    adr = []
    single_quote = '\''

    logging.info(dict_init)

    for b in dict_init['adr']:
        txt_ = f"Удалить {single_quote}{b[2]}{single_quote}"
        adr.append([{"text": txt_}])
        chat_user.gear_adr.append(txt_)

    adr.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    chat_user.gear_adr.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": adr, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_gear_del_city(dict_init, chat_user):
    city = []
    single_quote = '\''
    logging.info(dict_init)
    for b in dict_init['city']:
        if chat_user.__name__ in b[2]:
            txt_ = f"Исключить {single_quote}{b[1]}{single_quote}"
            city.append([{"text": txt_}])
            chat_user.gear_cities.append(txt_)
        else:
            pass

    city.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    chat_user.gear_cities.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": city, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_gear_add_city(dict_init, chat_user):
    city = []
    single_quote = '\''
    logging.info(dict_init)
    for b in dict_init['city']:
        if chat_user.__name__ in b[2]:
            pass
        else:
            txt_ = f"Добавить {single_quote}{b[1]}{single_quote}"
            city.append([{"text": txt_}])
            chat_user.gear_cities.append(txt_)

    city.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    chat_user.gear_cities.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": city, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_gear():
    # [{"text": f"Мой список городов", "callback_data": "gear_view"}, ],

    reply_markup = {"inline_keyboard": [
        [{"text": f"Добавить город", "callback_data": "gear_add_city"},
         {"text": f"Исключить город", "callback_data": "gear_del_city"}, ],
        [{"text": f"Удалить адрес у всех", "callback_data": "gear_del_address"}, ],
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return reply_markup


def template_fsm_region():
    new_region = []
    new_region.append([{"text": 'Добавить регион'}])

    reply_markup = {"keyboard": new_region,
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                    }
    return reply_markup


def template_fsm_city(dict_init, chat_user):
    city = []
    single_quote = '\''
    logging.info(dict_init)
    for b in dict_init['city']:
        if chat_user.__name__ in b[2]:
            txt_ = f"Привязать к {single_quote}{b[1]}{single_quote}"
            city.append([{"text": txt_}])
            chat_user.gear_cities.append(txt_)
        else:
            pass

    city.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    chat_user.gear_cities.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": city, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_fsm_address():
    new_adr = []
    new_adr.append([{"text": 'Добавить адрес'}])

    reply_markup = {"keyboard": new_adr,
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                    }
    return reply_markup


def template_start():
    r = emoji.emojize(u':two_o\u2019clock:')
    reply_markup = {"inline_keyboard": [[
        {"text": f"Время прибытия {r}", "callback_data": "region_arrived"},
        {"text": f"Мой список {emoji.emojize(':satellite:')}", "callback_data": "ent_list"}],
        [{"text": f"Мои города {emoji.emojize(':gear:')}", "callback_data": "gear"},
         {"text": f"Новый адрес {emoji.emojize(':Ukraine:')}", "callback_data": "add_address"}, ],
    ],
        "hide_keyboard": True,
    }

    return reply_markup


def template_remove_keboard():
    return {"remove_keyboard": True}


def template_hide_keboard():
    return {"hide_keyboard": True}


def template_weight(dict_init, chat_user):

    wt = []
    for b in dict_init['wt']:
        if chat_user.__name__ in b[2]:
            pass
        else:
            wt.append(
                {"text": str(b[1])}
            )
            chat_user.weight.append(str(b[1]))

    n = 3
    resize_wt = [wt[i:i+n] for i in range(0, len(wt), n)]
    logging.info(resize_wt)

    resize_wt.append([{"text": emoji.emojize(':BACK_arrow: Назад к перевозчикам')}])
    chat_user.weight.append(emoji.emojize(':BACK_arrow: Назад к перевозчикам'))

    reply_markup = {"keyboard": resize_wt, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_tasks_to_send(tmp_dict, chat_user):

    task_list = []

    for ts in tmp_dict:
        cnt = tmp_dict[ts]
        tmp_text = ', '.join([cnt['shop'], cnt['delivery'], cnt['weight'], cnt['dlv_time'], ])
        task_list.append([{"text": tmp_text}])
        chat_user.send_list.append(tmp_text)

    reply_markup = {"keyboard": task_list, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_edit_list():
    # logging.info(dict_init)

    reply_markup = {"inline_keyboard": [[
        {"text": f"Удалить из списка", "callback_data": "edit_list_send"},
        {"text": f"Удалить Все", "callback_data": "del_list_send"}],
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return reply_markup


def template_shops(dict_init, chat_user):
    adr = []

    for b in dict_init['adr']:
        location = b[0]

        for city in dict_init['city']:

            if location == city[0]:
                access = city[2]

                if chat_user.__name__ in access:
                    adr.append([{"text": b[2]}])
                    chat_user.adr.append(b[2])
                else:
                    pass

    adr.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    chat_user.adr.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": adr, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user


def template_delivery(dict_init, chat_user):
    dlv = []
    for b in dict_init['delivery']:
        if chat_user.__name__ in b[2]:
            pass
        else:
            dlv.append(
                {"text": b[1]}
            )
            chat_user.delivery.append(b[1])

    n = 2
    resize_dlv = [dlv[i:i+n] for i in range(0, len(dlv), n)]
    logging.info(resize_dlv)

    resize_dlv.append([{"text": emoji.emojize(':BACK_arrow: Назад к адресам')}])
    chat_user.delivery.append(emoji.emojize(':BACK_arrow: Назад к адресам'))

    reply_markup = {"keyboard": resize_dlv, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, chat_user
