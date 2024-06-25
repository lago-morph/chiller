# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from chiller_api.models.movie import Movie  # noqa: E501
from chiller_api.test import BaseTestCase


class TestSequence(BaseTestCase):
    """Test a sequence of operations"""

    def test_normal_processing(self):
        # create user with UUID
        # validate list of movies is empty
        # add several movies
        # validate list is what we expect
       
        pass

if __name__ == '__main__':
    import unittest
    unittest.main()
