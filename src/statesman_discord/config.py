__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
config.py
- settings for the flask application object
"""


import os
import random
import hashlib
import redis
from statesman_discord import constants


class BaseConfig(object):
    DEBUG = bool(os.environ.get(constants.DEBUG, True))
    PORT = int(os.environ.get(constants.PORT, "5000"))
    LOG_LEVEL = os.environ.get(constants.LOG_LEVEL, "INFO")
    SECRET_KEY = os.environ.get(constants.SECRET_KEY, hashlib.sha256(f"{random.random()}".encode("utf-8")).hexdigest())
    CSRF_TOKEN = os.environ.get(constants.CSRF_TOKEN, hashlib.sha256(f"{random.random()}".encode("utf-8")).hexdigest())
    CACHE_REDIS_HOST = os.environ[constants.REDIS_HOST]
    CACHE_REDIS_PORT = int(os.environ.get(constants.REDIS_PORT, "6379"))
    CACHE_REDIS_PASSWORD = os.environ.get(constants.REDIS_PW)
    CACHE_REDIS_DB = int(os.environ.get(constants.REDIS_DB, "7"))
    SESSION_TYPE = os.environ.get(constants.SESSION_TYPE, "redis")
    SESSION_REDIS = redis.from_url(f"redis://{os.environ[constants.REDIS_HOST]}:6379")
    EXECUTOR_TYPE = "thread"
    EXECUTOR_MAX_WORKERS = 5
    EXECUTOR_PROPAGATE_EXCEPTIONS = True
