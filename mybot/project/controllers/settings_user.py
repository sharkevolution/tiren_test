import emoji

dict_region = {'Днепр': {'Днепр': ['aaa']},
               'Львов': {'Львов': ['ddd']},
               'Одесса': {'Николаев': ['xxx'], 'Херсон': ['fff']},
               'Харьков': {},
               'Николаев': {},
               'Тернополь': {},
               'Запорожье': {},
               'Чернигов': {}
               }


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
         {"text": f"{ej_ok}", "callback_data": "ent_ok"}]
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False}

    return reply_markup


def template_city():
    reply_markup = {"keyboard": [[{"text": "Днепр"}],
                                 [{"text": "Львов"}],
                                 [{"text": "Одесса"}],
                                 [{"text": "Херсон"}],
                                 [{"text": "Николаев"}],
                                 [{"text": "Регион"}],
                                 [{"text": "Перевозчик"}],
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                    }

    return reply_markup


def template_delivery():
    reply_markup = {"keyboard": [[{"text": "ВИП"}],
                                 [{"text": "Координатор"}],
                                 [{"text": "Космос"}],
                                 [{"text": "Курьер"}],
                                 [{"text": "Регион"}],
                                 [{"text": "Город"}]
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                    }

    return reply_markup


def template_start():
    reply_markup = {"inline_keyboard": [[
        {"text": f"Время прибытия {emoji.emojize(':Ukraine:')}", "callback_data": "region_arrived"},
        {"text": f"К отправке {emoji.emojize(':cityscape:')}", "callback_data": "city"}],

        [{"text": f"Мои настройки {emoji.emojize(':delivery_truck:')}", "callback_data": "delivery"}, ],
    ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

    return reply_markup


def template_city():
    reply_markup = {"keyboard": [[{"text": "Звездец"}],
                                 [{"text": "Трындец"}],
                                 [{"text": "Перевозчик"}],
                                 ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                    }

    return reply_markup
