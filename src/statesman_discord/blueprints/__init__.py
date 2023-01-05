__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""


from functools import wraps
from flask import redirect, session, render_template, request
from statesman_discord import constants
import jinja2


def requires_auth(f):
    @wraps(f)
    def _check_auth(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            raise error_response
        if constants.PROFILE_KEY not in session:
            return redirect("/auth/login")
        return f(*args, **kwargs)

    return _check_auth


# def user_info(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if constants.PROFILE_KEY in session:
#             kwargs.update({
#                 'userinfo': session[constants.PROFILE_KEY],
#             })
#         return f(*args, **kwargs)

#     return decorated


def error_page(message, code):
    context = {
        "code": code,
        "message": message,
    }
    try:
        return render_page(f"errors/{code}.html")
    except jinja2.TemplateNotFound:
        return render_page("errors/error.html", context)


def render_page(page, context={}):

    show_cookie_message = True
    if request.cookies.get("cookies-accepted"):
        show_cookie_message = False

    userinfo = session.get(constants.PROFILE_KEY)
    if userinfo:
        context.update(
            {
                "showCookieMessage": show_cookie_message,
                "userinfo": userinfo,
            }
        )
    print(f"context: {context}")

    return render_template(page, **context)
