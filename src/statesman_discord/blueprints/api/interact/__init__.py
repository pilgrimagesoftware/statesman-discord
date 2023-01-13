__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
interact
- Interact API
"""

import logging
from datetime import datetime
from flask import session, jsonify, request, current_app, Blueprint
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from statesman_discord import constants
from statesman_discord.controllers.interact import handle_action_request, handle_ping, PingHandled
from statesman_discord.blueprints.api import user_required, requires_auth
from statesman_discord.blueprints.api.exceptions import error_response
from statesman_discord.common.exceptions import SignatureException
from statesman_discord.utils.limiter import limiter


blueprint = Blueprint("interact", __name__, url_prefix="/interact")


@blueprint.route("/", methods=["POST"])
@limiter.limit("10/second")
def handle_interaction():
    logging.debug("POST /interact/: %s", request)

    try:
        handle_ping(request)
        return handle_action_request(request)
    except PingHandled:
        logging.info("Handled ping request.")
        return jsonify({"type": 1}), 200
    except SignatureException:
        logging.info("Signature verification failed.")
        return jsonify({}), 401
    except:
        logging.exception("Exception while processing interaction")
        response = {"response_type": "ephemeral", "text": "Sorry, that didn't work. Please try again."}

        return response, 200
