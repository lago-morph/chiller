import connexion
import six

import string
import jwt

from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api import util
from chiller_api.validation import ValidationError

from chiller_api.db import queries


def validate_user_payload(user):


    if len(user.name) == 0:
        raise ValidationError('zero length name in JSON object', 400)

    allowed = set(string.ascii_lowercase 
                    + string.ascii_uppercase 
                    + string.digits)
    if not (set(user.name) <= allowed):
        raise ValidationError(
                'name can only have alphabetic characters and digits', 400)

def create_user(body=None):  # noqa: E501
    """Create a new user
    """

    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return 'no user JSON object in request', 400

    if user.name is None:
        return 'username key not set in JSON object', 400

    try:
        validate_user_payload(user)
    except ValidationError as e:
        return e.msg, e.code

    if queries.add_user(user.name):
        return 'user created', 201
    else:
        return 'duplicate user name', 403


def login_user(user_name):  # noqa: E501
    """Log in as user
    """

    if user_name is None:
        return 'username key not set in JSON object', 400

    user = User(name=user_name)
    try:
        validate_user_payload(user)
    except ValidationError as e:
        return e.msg, e.code

    user.id = queries.get_user_id(user_name)

    if user.id is None:
        return 'username not found', 403

    # yeah, I'll change this later when we actually CHECK this is valid...
    key = "secret"
    encoded = jwt.encode(user.to_dict(), key, algorithm="HS256")

    return JWT(token = encoded), 200

