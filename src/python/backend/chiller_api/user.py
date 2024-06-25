from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api import util

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/create")
def create(body=None):  # noqa: E501
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login(user_name):  # noqa: E501
    """Log in as user

    Log in as the specified user and get the authentication token # noqa: E501

    :param user_name: Username
    :type user_name: str

    :rtype: JWT
    """
    return 'do some magic!'
