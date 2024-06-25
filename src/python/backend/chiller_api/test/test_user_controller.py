# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create a new user
        """
        body = User()
        response = self.client.open(
            '/user/create',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user

        Log in as user
        """
        response = self.client.open(
            '/user/login/{username}'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
