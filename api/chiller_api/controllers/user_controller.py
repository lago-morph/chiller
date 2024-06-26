import connexion
import six

from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api import util


def create_user(body=None):  # noqa: E501
    """Create a new user

     # noqa: E501

    :param body: User to create
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login_user(user_name):  # noqa: E501
    """Log in as user

    Log in as the specified user and get the authentication token # noqa: E501

    :param user_name: Username
    :type user_name: str

    :rtype: JWT
    """
    return 'do some magic!'
