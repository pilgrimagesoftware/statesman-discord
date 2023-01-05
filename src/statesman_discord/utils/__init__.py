__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Utilities
"""


import json
from typing import Any
# from bson.timestamp import Timestamp
import base64
import os.path
import pkgutil
import importlib


def get_package_modules(package:str) -> list:
    # pkgpath = package os.path.dirname(testpkg.__file__)
    module = importlib.import_module(package)
    pkgpath = os.path.dirname(module.__file__)
    modules = [f'{package}.{name}' for _, name, _ in pkgutil.iter_modules([pkgpath])]
    return list(set(modules)).sort()


def build_error_blocks(msg:str) -> list:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"❗️ {msg} 😢",
            }
        },
    ]

    return blocks


def build_message_blocks(msg:str) -> list:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"✅ {msg} 👍🏼",
            }
        },
    ]

    return blocks


class SafeEncoder(json.JSONEncoder):
    """
    """

    def default(self, o: Any) -> Any:
        # if isinstance(o, Timestamp):
        #     return str(o.as_datetime())
        if isinstance(o, bytes):
            return base64.b64encode(o).decode('utf-8')
        return json.JSONEncoder.default(self, o)
