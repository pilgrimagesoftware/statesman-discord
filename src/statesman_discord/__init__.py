__author__ = "Paul Schifferer <paul@schifferers.net>"
__version__ = "1.0.2"
"""
"""

import sentry_sdk
import os
from statesman_discord import constants
from sentry_sdk.integrations.redis import RedisIntegration
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


sentry_dsn = os.environ.get(constants.SENTRY_DSN)
if sentry_dsn is not None:
    sentry_sdk.init(dsn=sentry_dsn, environment=os.environ.get(constants.SENTRY_ENV, "Development"), integrations=[])
