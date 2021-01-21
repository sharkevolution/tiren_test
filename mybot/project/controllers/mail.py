#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import gmail
from gmail import Message


def send_mail(base_mail, to_mail, user_name, user_text):
    # try:
    b = "".join(["Thanks 2018! <", base_mail, ">"])

    gm = gmail.GMail(b, 'fortuna-3#')
    msg = Message('Спасибо от', to="me <{0}>".format(to_mail),
                  text="Спасибо от {0}, сообщение: {1}".format(user_name, user_text))
    gm.send(msg)
    # except Exception as ex:
    #     pass

# def send_mail_key(base_mail, base_mailpass, to_mail, akey):
#
#     b = "".join(["sharkevo <", base_mail, ">"])
#     txt = "".join(["Для завершения регистрации и начала работы ",
#                    "введите указанный код активации на сайте: ",
#                    akey])
#
#     gm = gmail.GMail(b, base_mailpass)
#     msg = Message('Завершение регистрации', to="me <{0}>".format(to_mail), text=txt)
#     gm.send(msg)

    "tgxm8ou"


def send_sms(user_name, user_text):

    try:

        # Отправка сообщения пользователю
        login = '380732218247'  # phone number
        password = 'tgxm8ou'  # Password
        alphaName = 'gsm1'  # string, sender id (alpha-name)

        abonent = '380732218247'
        text = '2018 Thanks!: name: {0}, txt: {1}'.format(user_name, user_text)

        xml = "<?xml version='1.0' encoding='utf-8'?><request_sendsms><username><![CDATA[" + \
              login + "]]></username><password><![CDATA[" + password + "]]></password><from><![CDATA[" + \
              alphaName + "]]></from><to><![CDATA[" + abonent + "]]></to><text><![CDATA[" + \
              text + "]]></text></request_sendsms>"

        url = 'https://gate.smsclub.mobi/xml/'
        headers = {'Content-type': 'text/xml; charset=utf-8'}

        try:
            res = requests.post(url, data=xml, headers=headers)
        except:
            pass
            # print(res.status_code)
            # print(res.raise_for_status())

    except Exception as ex:
        pass