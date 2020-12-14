
import os
import logging
import redis
import msgpack


def variable_init():

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    if redisClient.exists("settings_data"):
        logging.info('YES')


def clear_base_redis():
    # Clear base Redis
    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    for key in redisClient.keys('*'):
        redisClient.delete(key)
    pass


def get_redis_message(chat_id):
    """ Add to Redis last message Bot """
    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    res = {}
    if redisClient.exists(chat_id):
        res = msgpack.unpackb(redisClient.get(chat_id))
        logging.info(res)
    return res


def put_redis_message_user(data):
    """ Add to Redis last message User """

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    chat_id = data['message']['chat']['id']
    sms_id_last_user = data['message']['from']['id']

    if base_keys := get_redis_message(chat_id):
        base_keys['sms_id_last_user'] = sms_id_last_user
    else:
        base_keys = {'sms_id_last_user': sms_id_last_user}

    new_pack = msgpack.packb(base_keys)
    # logging.info(base_keys)
    # logging.info(new_pack)
    redisClient.set(chat_id, new_pack)


def put_redis_message_bot(data, id_sms):
    """ Add to Redis last message Bot """

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    chat_id = data['result']['chat']['id']

    if base_keys := get_redis_message(chat_id):
        base_keys['sms_id_last_bot'] = id_sms
    else:
        base_keys = {'sms_id_last_bot': id_sms}

    new_pack = msgpack.packb(base_keys)
    # logging.info('SAVE !!!')
    # logging.info(base_keys)
    redisClient.set(chat_id, new_pack)