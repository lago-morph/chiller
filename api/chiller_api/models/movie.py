# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from chiller_api.models.base_model_ import Model
from chiller_api import util


class Movie(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None):  # noqa: E501
        """Movie - a model defined in Swagger

        :param name: The name of this Movie.  # noqa: E501
        :type name: str
        """
        self.swagger_types = {
            'name': str
        }

        self.attribute_map = {
            'name': 'name'
        }
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'Movie':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Movie of this Movie.  # noqa: E501
        :rtype: Movie
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Movie.

        The name of the movie  # noqa: E501

        :return: The name of this Movie.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Movie.

        The name of the movie  # noqa: E501

        :param name: The name of this Movie.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name
