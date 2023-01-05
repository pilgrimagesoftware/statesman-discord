__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
- API
"""


from functools import wraps
from flask import Blueprint, request, render_template, session, jsonify, current_app
from werkzeug.exceptions import HTTPException
import logging
import json
import os
from statesman_discord import constants
from statesman_discord.models import constants as model_constants
from statesman_discord.blueprints import render_page, requires_auth
from statesman_discord.blueprints.api.exceptions import error_response
from werkzeug.exceptions import Unauthorized, BadRequest, Forbidden


class UserAuthorizationException(Exception):
    def __init__(self, reason: str):
        self.reason = reason


def _check_user():
    # check body payload
    data = request.get_json()
    logging.debug("data: %s", data)
    user_id = None
    if data is not None:
        user_id = data.get("user")
        logging.debug("user_id: %s", user_id)

    if user_id is None:
        # check headers: X-User-ID
        user_id = request.headers.get("X-User-ID")
        logging.debug("user_id: %s", user_id)

    # user_id = session.get(constants.CURRENT_USER_ID)
    # if user_id:
    #     user = User.query.filter_by(id=user_id).first()
    #     if user:
    #         if has_role(user, role_name):
    #             return user

    #         raise UserAuthorizationException('insufficient permissions')

    #     raise UserAuthorizationException('user not found')

    # raise UserAuthorizationException('no user in session')
    return user_id


def requires_auth(f):
    @wraps(f)
    def _check_auth(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            raise error_response(Unauthorized, "unauthorized", f"The endpoint requires authorization")
        auth_parts = auth_header.split(" ", maxsplit=2)
        if len(auth_parts) != 2:
            raise error_response(BadRequest, "bad_request", f"Invalid Authorization header")
        if auth_parts[0].lower() != "bearer":
            raise error_response(Forbidden, "forbidden", f"Authorization method not accepted")
        if auth_parts[1] != os.environ[constants.CLIENT_AUTH_TOKEN]:
            raise error_response(Forbidden, "forbidden", f"Authorization token not accepted")
        return f(*args, **kwargs)

    return _check_auth


# def admin_required(f):
#     @wraps(f)
#     def _get_user(*args, **kwargs):
#         try:
#             user = _check_user()
#             return f(user, *args, **kwargs)
#         except UserAuthorizationException as e:
#             return jsonify({
#                 'error': "Unauthorized; " + e.reason
#             }), 401

#     return _get_user


def user_required(f):
    @wraps(f)
    def _get_user(*args, **kwargs):
        try:
            user = _check_user()
            return f(user, *args, **kwargs)
        except UserAuthorizationException as e:
            return jsonify({"error": "Unauthorized; " + e.reason}), 401

    return _get_user


def user_optional(f):
    @wraps(f)
    def _get_user(*args, **kwargs):
        try:
            user = _check_user()
            return f(user, *args, **kwargs)
        except UserAuthorizationException as e:
            return f(None, *args, **kwargs)

    return _get_user


# @blueprint.errorhandler(Exception)
# def error_handler(ex):
#     current_app.logger.exception(f"Exception caught: {ex}")
#     response = jsonify(message=str(ex))
#     response.status_code = ex.code if isinstance(ex, HTTPException) else 500
#     return response


# from statesman_discord.blueprints.api.interact import interact
# from statesman_discord.blueprints.api.verify import verify
