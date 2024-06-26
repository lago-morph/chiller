# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from chiller_api.models.base_model_ import Model
from chiller_api import util


class JWT(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, token: str=None):  # noqa: E501
        """JWT - a model defined in Swagger

        :param token: The token of this JWT.  # noqa: E501
        :type token: str
        """
        self.swagger_types = {
            'token': str
        }

        self.attribute_map = {
            'token': 'token'
        }
        self._token = token

    @classmethod
    def from_dict(cls, dikt) -> 'JWT':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The JWT of this JWT.  # noqa: E501
        :rtype: JWT
        """
        return util.deserialize_model(dikt, cls)

    @property
    def token(self) -> str:
        """Gets the token of this JWT.

        JWT token  # noqa: E501

        :return: The token of this JWT.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token: str):
        """Sets the token of this JWT.

        JWT token  # noqa: E501

        :param token: The token of this JWT.
        :type token: str
        """
        if token is None:
            raise ValueError("Invalid value for `token`, must not be `None`")  # noqa: E501

        self._token = token
