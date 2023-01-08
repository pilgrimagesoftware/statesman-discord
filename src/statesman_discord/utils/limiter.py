__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(get_remote_address)
