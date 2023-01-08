__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
signature.py
- Discord signature verification
"""


from flask import current_app
import os, logging
from statesman_discord import constants
from statesman_discord.common.exceptions import SignatureException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def verify_signature(signature: str, timestamp: str, request_body: str):
    logging.debug("signature: %s", signature)

    logging.debug("request_body: %s", request_body)
    # our_sig = f'{constants.SLACK_SIGNATURE_VERSION}:{timestamp}:{request_body}'
    # logging.debug("our_sig: %s", our_sig)

    key = os.environ[constants.DISCORD_PUBLIC_KEY]
    logging.debug("key: %s", key)
    verify_key = VerifyKey(bytes.fromhex(key))

    try:
        verify_key.verify(f"{timestamp}{request_body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        # abort(401, 'invalid request signature')
        # if f'{constants.SLACK_SIGNATURE_VERSION}={digest}' != signature:
        raise SignatureException("Signature failed validation")
