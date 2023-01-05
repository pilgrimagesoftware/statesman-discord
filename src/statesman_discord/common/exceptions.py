__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""


class ForbiddenException(Exception):
    pass

class NotFoundException(Exception):
    pass

class ActionNotSupportedException(Exception):
    pass

class SignatureException(Exception):
    pass
