__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
utils.py
- Utility APIs
"""


from flask import session, jsonify, request, current_app
from statesman_discord.blueprints.api import blueprint
import json
import random


# @blueprint.route('/random/name', methods=['GET'])
# def random_name():
#     current_app.logger.debug(f"GET /random/name: {request}")
#     name_type = request.args.get('type')
#     if not name_type:
#         return {}

#     with open(f'/{current_app.static_folder}/{name_type}-names.json', 'r') as n:
#         names = json.load(n)
#         name = random.choice(names)

#         return {
#             'name': name,
#         }
