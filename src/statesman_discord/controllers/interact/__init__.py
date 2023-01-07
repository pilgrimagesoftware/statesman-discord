__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
interact
- Interaction controller
"""


from flask import current_app
import json
import os
from statesman_discord import constants
from statesman_discord.utils.discord.signature import verify_signature
from statesman_discord.common.exceptions import SignatureException


class PingHandled(Exception):
    pass


class PayloadException(Exception):
    pass


def handle_action_request(request: object):
    current_app.logger.debug("request: %s", request)

    # content_length = request.headers.get('content-length')
    body = request.get_data().decode("utf-8")
    current_app.logger.debug("body: %s", body)

    current_app.logger.debug("headers: %s", request.headers)
    current_app.logger.debug("args: %s", request.args)
    current_app.logger.debug("form: %s", request.form)
    current_app.logger.debug("cookies: %s", request.cookies)

    signature = request.headers.get("x-signature-ed25519")
    current_app.logger.debug("signature: %s", signature)
    if signature is None or len(signature) == 0:
        raise SignatureException("Missing or empty signature header.")
    timestamp = request.headers.get("x-signature-timestamp")
    current_app.logger.debug("timestamp: %s", timestamp)
    if timestamp is None or len(timestamp) == 0:
        raise SignatureException("Missing or empty timestamp.")
    # validate signature
    verify_signature(signature, timestamp, body)

    # TODO


def handle_ping(request: object):
    current_app.logger.debug("request: %s", request)

    body = request.get_data().decode("utf-8")
    current_app.logger.debug("body: %s", body)

    msg = json.loads(body)
    msg_type = msg.get("type")
    if msg_type != 1:
        return

    if msg.get("application_id") != os.environ[constants.DISCORD_CLIENT_ID]:
        current_app.logger.warn("Application ID in incoming payload did not match ours.")
        raise PayloadException("'application_id' in payload did not match ours.")

    signature = request.headers.get("x-signature-ed25519")
    current_app.logger.debug("signature: %s", signature)
    if signature is None or len(signature) == 0:
        raise SignatureException("Missing or empty signature header.")
    timestamp = request.headers.get("x-signature-timestamp")
    current_app.logger.debug("timestamp: %s", timestamp)
    if timestamp is None or len(timestamp) == 0:
        raise SignatureException("Missing or empty timestamp.")
    # validate signature
    verify_signature(signature, timestamp, body)

    raise PingHandled()
