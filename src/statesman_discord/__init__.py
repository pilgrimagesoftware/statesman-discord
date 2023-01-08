__author__ = "Paul Schifferer <paul@schifferers.net>"
__version__ = "1.0.38"
"""
"""

import sentry_sdk
import os
from statesman_discord import constants
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


sentry_sdk.init(
    dsn=os.environ[constants.SENTRY_DSN],
    environment=os.environ.get(constants.SENTRY_ENV) or "Development",
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0,
    _experiments={
        "profiles_sample_rate": 1.0,
    },
)
