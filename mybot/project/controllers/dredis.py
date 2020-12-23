import os
import json
import logging
import redis
import msgpack

from mybot.config import RESOURCES_PATH


def variable_init(bot):
    """
        Load Data from data.txt (json) and save or get data from redis variable
    """
    redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    if redisClient.exists("settings_data"):
        bot.dict_init = msgpack.unpackb(redisClient.get('settings_data'))
        # logging.info(bot.dict_init)
    else:
        file_path = [RESOURCES_PATH, 'settings', 'data.txt']
        djs = os.path.join(*file_path)

        with open(djs) as json_file:
            newDict = json.load(json_file)

        # save to redis
        redisClient.set('settings_data', msgpack.packb(newDict))


def save_variable(newDict):

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))

    if redisClient.exists("settings_data"):
        # save to redis
        redisClient.set('settings_data', msgpack.packb(newDict))




def clear_base_redis():
    ## Clear base Redis

    redisClient = redis.from_url(os.environ.get("REDIS_URL"))
    for key in redisClient.keys('*'):
        redisClient.delete(key)
