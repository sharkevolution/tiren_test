import emoji
import logging


# [{"text": f"Мои перевозчики {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Удалить время прибытия {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Удалить регионы {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Удалить города {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
# [{"text": f"Мои города {emoji.emojize(':shopping_cart:')}", "callback_data": "delivery"}, ],
# [{"text": f"Мои адреса {emoji.emojize(':shopping_cart:')}", "callback_data": "shop"}, ],
# [{"text": f"Настройки бота {emoji.emojize(':shopping_cart:')}", "callback_data": "shop"}, ],


def template_engineer_mode():
    ej_ok = emoji.emojize(':OK_button:')

    reply_markup = {"inline_keyboard": [[
        {"text": f"{emoji.emojize(' 1 ')}", "callback_data": "ent_one"},
        {"text": f"{emoji.emojize(' 2 ')}", "callback_data": "ent_two"},
        {"text": f"{emoji.emojize(' 3 ')}", "callback_data": "ent_three"}],

        [{"text": f"{emoji.emojize(' 4 ')}", "callback_data": "ent_four"},
         {"text": f"{emoji.emojize(' 5 ')}", "callback_data": "ent_five"},
         {"text": f"{emoji.emojize(' 6 ')}", "callback_data": "ent_six"}],

        [{"text": f"{emoji.emojize(' 7 ')}", "callback_data": "ent_seven"},
         {"text": f"{emoji.emojize(' 8 ')}", "callback_data": "ent_eight"},
         {"text": f"{emoji.emojize(' 9 ')}", "callback_data": "ent_nine"}],

        [{"text": f"{emoji.emojize(' 0 ')}", "callback_data": "ent_zero"},
         {"text": f"{emoji.emojize(' : ')}", "callback_data": "ent_three"}
         {"text": f"{emoji.emojize(':skull_and_crossbones:')}", "callback_data": "ent_ok"}],

        [{"text": f"{emoji.emojize('Enter')}", "callback_data": "ent_ok"}],
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False}

    return reply_markup


def template_start():
    r = emoji.emojize(u':two_o\u2019clock:')
    reply_markup = {"inline_keyboard": [[
        {"text": f"Время прибытия {r}", "callback_data": "region_arrived"},
        {"text": f"К отправке {emoji.emojize(':satellite:')}", "callback_data": "send_to"}],
        [{"text": f"Мои настройки {emoji.emojize(':gear:')}", "callback_data": "gear"}, ],
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return reply_markup


def template_weight(dict_init, chat_user):

    wt = []
    for b in dict_init['wt']:
        if chat_user.__name__ in b[2]:
            pass
        else:
            wt.append([{"text": str(b[1])}])
            chat_user.weight.append(str(b[1]))

    reply_markup = {"keyboard": wt,
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    return reply_markup, chat_user


def template_region_all():
    ej_ukraine = emoji.emojize(':Ukraine:')
    ej_city = emoji.emojize(':cityscape:')
    ej_delivery = emoji.emojize(':delivery_truck:')
    ej_shop = emoji.emojize(':shopping_cart:')

    reply_markup = {"inline_keyboard": [[
        {"text": f"Регион {ej_ukraine}", "callback_data": "region"},
        {"text": f"Город {ej_city}", "callback_data": "city"}],
        [{"text": f"Магазин {ej_shop}", "callback_data": "shop"}, ],
        [{"text": f"Перевозчик {ej_delivery}", "callback_data": "delivery"}, ]
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False}

    return reply_markup


def template_shops(dict_init, chat_user):
    adr = []
    # logging.info(dict_init)
    for b in dict_init['adr']:
        if chat_user.__name__ in b[3]:
            pass
        else:
            adr.append([{"text": b[2]}])
            chat_user.adr.append(b[2])

    adr.append([{"text": 'Update'}])
    chat_user.delivery.append('Update')

    reply_markup = {"keyboard": adr,
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    return reply_markup, chat_user


def template_delivery(dict_init, chat_user):
    dlv = []
    for b in dict_init['delivery']:
        if chat_user.__name__ in b[2]:
            pass
        else:
            dlv.append([{"text": b[1]}])
            chat_user.delivery.append(b[1])

    dlv.append([{"text": emoji.emojize(':BACK_arrow:')}])
    chat_user.delivery.append(emoji.emojize(':BACK_arrow:'))

    reply_markup = {"keyboard": dlv,
                    "resize_keyboard": True,
                    "one_time_keyboard": False}

    return reply_markup, chat_user
