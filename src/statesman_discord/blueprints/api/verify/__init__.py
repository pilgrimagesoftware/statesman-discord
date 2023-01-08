__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
verify.py
- Verify API
"""


import logging
from datetime import datetime
from flask import session, jsonify, request, current_app, Blueprint
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from statesman_discord import constants
from statesman_discord.controllers.interact import handle_action_request
from statesman_discord.models import constants as model_constants
from statesman_discord.blueprints.api import user_required, requires_auth
from statesman_discord.blueprints.api.exceptions import error_response
from statesman_discord.common.exceptions import SignatureException


blueprint = Blueprint("verify", __name__, url_prefix="/verify")


@blueprint.route("/", methods=["POST"])
def handle_verify():
    logging.debug("POST /verify/: %s", request)

    try:
        # handle_ssl_check(request)
        return handle_action_request(request)
    except:
        logging.exception("Exception while processing verification")
        response = {"response_type": "ephemeral", "text": "Sorry, that didn't work. Please try again."}

        return response, 200
