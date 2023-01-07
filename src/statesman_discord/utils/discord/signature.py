__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
signature.py
- Discord signature verification
"""


from flask import current_app
import os
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
        verify_key.verify(f"{timestamp}{request_body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        # abort(401, 'invalid request signature')
        # if f'{constants.SLACK_SIGNATURE_VERSION}={digest}' != signature:
        raise SignatureException("Signature failed validation")
