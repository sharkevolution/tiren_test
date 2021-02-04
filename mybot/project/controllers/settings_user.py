import emoji
import logging


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
    reply_markup = {"inline_keyboard": [
        [{"text": f"Добавить город", "callback_data": "gear_add_city"},
         {"text": f"Исключить город", "callback_data": "gear_del_city"}, ],
        [{"text": f"Удалить адрес у всех", "callback_data": "gear_del_address"}, ],
        [{"text": f"Список пользователей", "callback_data": "gear_list_users"}, ]
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
        txt_ = f"Привязать к {single_quote}{b[1]}{single_quote}"
        city.append([{"text": txt_}])
        chat_user.bind_to_city.append(txt_)

    city.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    chat_user.bind_to_city.append(emoji.emojize(':TOP_arrow: На главную'))

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
        [{"text": f"Консолидировать данные", "callback_data": "aggregate"}, ]
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


def template_tasks_to_send(tmp_dict, chat_user, rdot):

    task_list = []

    for ts in tmp_dict:
        cnt = tmp_dict[ts]
        if rdot in ts:
            tmp_text = cnt
        else:
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


def change_status_subscription(bot, chat_user):

    logging.info('change_status_subscription')

    if uid := bot.subscription.get(chat_user.selected_subscriber):

        for chunk in chat_user.selected_sub_data:
            st = chat_user.selected_sub_data[chunk]
            st['status_send'] = 'combined'
            chat_user.selected_sub_data[chunk] = st

            for f in uid:

                logging.info(f[0])
                logging.info(chat_user.selected_change_datetime)

                if f[0] == chat_user.selected_change_datetime:
                    shops = f[1]
                    for h in shops:
                        st = shops[h]
                        st['status_send'] = 'combined'
                        shops[h] = st

                    f[1] = shops

    bot.subscription[chat_user.selected_subscriber] = uid


def template_sub_print(bot, chat_user, ord):
    users_text = []
    commands_ = []
    dlv = []
    result_text = 'Список пуст'

    # logging.info(bot.subscription)

    if uid := bot.subscription.get(chat_user.selected_subscriber):
        for chunk in uid:
            # logging.info(ord)
            # logging.info(chunk[0])

            shops = chunk[1]
            txt = ''

            for h in shops:
                st = shops[h]
                logging.info(st['status_send'])
                if st['status_send'] == 'pending':
                    txt = chunk[0] + emoji.emojize('  :zzz:')
                    break
                if st['status_send'] == 'combined':
                    txt = chunk[0] + emoji.emojize('  :check_mark:')
                    break
                if st['status_send'] == 'rejected':
                    txt = chunk[0] + emoji.emojize('  :cross_mark:')
                    break

            # if chunk[0] == ord:
            if txt == ord:
                temp_ = chunk[1]
                for k in temp_:
                    users_text.insert(0, ' '.join([k]))
                    result_text = '\n'.join(users_text)

                    chat_user.selected_sub_data[k] = temp_[k]
                    logging.info(temp_[k])
            else:
                logging.info('not data')

    dlv.extend([{"text": 'Принять'}, {"text": 'Отклонить'}, {"text": 'К датам'}])

    n = 2
    resize_dlv = [dlv[i:i+n] for i in range(0, len(dlv), n)]
    logging.info(resize_dlv)

    resize_dlv.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])

    commands_.extend(['Принять', 'Отклонить', 'К датам'])
    commands_.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": resize_dlv, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, commands_, result_text


def template_sub_datetime(bot, chat_user, ord):
    users_messages = []
    commands_ = []

    logging.info(bot.subscription)
    logging.info(ord)

    for b in bot.subscription:
        if me := bot.users.get(int(b)):
            username = ' '.join([me.first_name, me.last_name, b])
            if username == ord:

                # Выбранный подписчик
                chat_user.selected_subscriber = b
                # logging.info(b)

                for userdata in bot.subscription[b]:
                    # logging.info(userdata)

                    shops = userdata[1]
                    txt = ''

                    for h in shops:
                        st = shops[h]
                        logging.info(st['status_send'])
                        if st['status_send'] == 'pending':
                            txt = userdata[0] + emoji.emojize('  :zzz:')
                            break
                        if st['status_send'] == 'combined':
                            txt = userdata[0] + emoji.emojize('  :check_mark:')
                            break
                        if st['status_send'] == 'rejected':
                            txt = userdata[0] + emoji.emojize('  :cross_mark:')
                            break

                    users_messages.append([{"text": txt}])
                    commands_.append(txt)
        else:
            logging.info('not data')

    users_messages.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    commands_.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": users_messages, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, commands_


def template_subscription(bot):
    users_list = []
    commands_ = []

    for b in bot.subscription:
        if me := bot.users.get(int(b)):
            username = ' '.join([me.first_name, me.last_name, b])
            users_list.append([{"text": username}])
            commands_.append(username)
        else:
            pass

    users_list.append([{"text": emoji.emojize(':TOP_arrow: На главную')}])
    commands_.append(emoji.emojize(':TOP_arrow: На главную'))

    reply_markup = {"keyboard": users_list, "resize_keyboard": True, "one_time_keyboard": False}

    return reply_markup, commands_


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
