import connexion
import six

import string

from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api import util

from chiller_api.db import queries


def create_user(body=None):  # noqa: E501
    """Create a new user

     # noqa: E501

    :param body: User to create
    :type body: dict | bytes

    :rtype: User
    """
    # an empty data field gives a 400 response before we get here
    #if connexion.request is None:
    #    return 'no POST data in request', 400

    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return 'no user JSON object in request', 400

    if body.name is None:
        return 'username key not set in JSON object', 400

    if len(body.name) == 0:
        return 'zero length name in JSON object', 400

    allowed = set(string.ascii_lowercase 
                    + string.ascii_uppercase 
                    + string.digits)
    if not (set(body.name) <= allowed):
        return 'name can only have alphabetic characters and digits', 400

    if queries.add_user(body.name):
        return 'user created', 201
    else:
        return 'duplicate user name', 403


def login_user(user_name):  # noqa: E501
    """Log in as user

    Log in as the specified user and get the authentication token # noqa: E501

    :param user_name: Username
    :type user_name: str

    :rtype: JWT
    """
    return 'do some magic!'
