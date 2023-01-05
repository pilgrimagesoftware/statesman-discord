__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
validators.py
- Validators for API calls
"""


from flask import current_app
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from functools import wraps
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from statesman_discord.blueprints.api.exceptions import error_response
# from application.utils.users import filtered_server


# def validate_server(server_id:str, user:str):
#     current_app.logger.info(f"Validating server {server_id} for user {user}.")

#     server = filtered_server(server_id, user)
#     if server is None:
#         raise error_response(NotFound, 'not_found',
#                              f"The server could not be found")

#     if len(server) == 0:
#         raise error_response(Forbidden, 'forbidden',
#                              f"The user {user} is not allowed access to server {server_id}.")

#     return server


# def validate_payload(validator, request: object):
#     current_app.logger.info(f"Validating request {request} using {validator}.")
#     inputs = validator(request)
#     current_app.logger.debug(f"inputs: {inputs}")
#     if not inputs.validate():
#         current_app.logger.debug(f"errors: {inputs.errors}")
#         raise BadRequest(inputs.errors)

#     current_app.logger.info("Payload is valid.")


# def validate_user(obj, user):
#     if not obj:
#         raise error_response(NotFound, 'not_found',
#                              f"The object could not be found")
#     if obj.creator_id != user.id:
#         raise error_response(Forbidden, 'forbidden',
#                              "You are not allowed to modify this object")


# def check_dependent_object(obj, attribute_name):
#     if not obj:
#         raise error_response(BadRequest, 'not_found',
#                              "Object not found", attribute=attribute_name)
