__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask, session
from flask_session import Session
from statesman_discord import constants
from logging.config import dictConfig
from statesman_discord.blueprints import error_page
from werkzeug.exceptions import HTTPException
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
from flask_executor import Executor
import os, logging
from statesman_discord.utils.leader_election import LeaderElection


# def _leaderelection_filter(level):
#     level = getattr(logging, level)

#     def filter(record):
#         return record.levelno <= level

#     return filter


def create_app(app_name=constants.APPLICATION_NAME):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s %(pathname)s %(funcName)s, line %(lineno)d: %(message)s",
                }
            },
            # "filters": {"leaderelection": {"()": "statesman_discord.main._leaderelection_filter", "level": "WARNING"}},
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "default"}},
            "root": {"level": os.environ.get(constants.LOG_LEVEL, "INFO"), "handlers": ["wsgi"]},
        }
    )

    app = Flask(app_name)
    app.config.from_object("statesman_discord.config.BaseConfig")
    # env = DotEnv(app)
    # cache.init_app(app)

    app.session = Session(app)

    from statesman_discord.utils.limiter import limiter

    limiter.init_app(app)

    app.sentry = SentryWsgiMiddleware(app)

    app.executor = Executor(app)

    app.leader_election = LeaderElection()

    from statesman_discord.blueprints.api.interact import blueprint as interact_blueprint

    app.register_blueprint(interact_blueprint)

    from statesman_discord.blueprints.api.verify import blueprint as verify_blueprint

    app.register_blueprint(verify_blueprint)

    from statesman_discord.blueprints.health import blueprint as health_blueprint

    app.register_blueprint(health_blueprint)

    from statesman_discord.messaging import consumer_thread

    app.consumer_thread = consumer_thread

    print(app.url_map)

    return app
