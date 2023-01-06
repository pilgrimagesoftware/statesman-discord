__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
discord.py
- Discord utilities
"""


from flask import current_app
import subprocess, shlex
import json
import hmac, hashlib
import os
import logging
import requests
from statesman_discord import constants
from statesman_discord.common.exceptions import SignatureException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def verify_signature(signature: str, timestamp: str, request_body: str):
    current_app.logger.debug("signature: %s", signature)

    current_app.logger.debug("request_body: %s", request_body)
    # our_sig = f'{constants.SLACK_SIGNATURE_VERSION}:{timestamp}:{request_body}'
    # current_app.logger.debug("our_sig: %s", our_sig)

    key = os.environ[constants.DISCORD_PUBLIC_KEY]
    current_app.logger.debug("key: %s", key)
    verify_key = VerifyKey(bytes.fromhex(key))

    try:
        verify_key.verify(f'{timestamp}{request_body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        # abort(401, 'invalid request signature')
        # if f'{constants.SLACK_SIGNATURE_VERSION}={digest}' != signature:
        raise SignatureException('Signature failed validation')


def send_message(response_url: str, blocks: list, private: bool):
    current_app.logger.debug("response_url: %s, blocks: %s, private: %s", response_url, blocks, private)

    response_type = "in_channel" if not private else "ephemeral"

    body = json.dumps(
        {
            "response_type": response_type,
            "blocks": blocks,
        }
    )
    current_app.logger.debug("body: %s", body)
    r = requests.post(
        response_url,
        headers={
            "Content-type": "application/json",
        },
        data=body,
    )
    current_app.logger.debug("r: %s", r)
