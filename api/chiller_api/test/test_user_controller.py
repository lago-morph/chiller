# coding: utf-8

from __future__ import absolute_import

from flask import json, current_app
from six import BytesIO

from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api.test import BaseTestCase

from chiller_api.db import queries


class TestUserControllerCreateSuccess(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create a new user
        """
        body = User(name="bob")
        response = self.client.open(
            '/user/create',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert201(response,
                       'Response body is : ' + response.data.decode('utf-8'))

class TestUserControllerCreateError(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ct = 'application/json'

    def test_create_user_duplicate(self):
        duplicate = "duplicate"
        queries.add_user(duplicate)
        d = json.dumps(User(name=duplicate))
        self.assert403(
            self.client.post('/user/create', data=d, content_type=self.ct))

    def test_create_user_empty_body(self):
    # empty body
        d = None
        self.assert400(
            self.client.post('/user/create', data=d, content_type=self.ct))
    
    # empty JSON object
    def test_create_user_empty_json_object(self):
        d = '{ }'
        self.assert400(
            self.client.post('/user/create', data=d, content_type=self.ct))

    # name not in JSON payload
    def test_create_user_missing_name_key(self):
        d = '{"key1": "value", "key2": 3}'
        self.assert400(
            self.client.post('/user/create', data=d, content_type=self.ct))

    # body is not parsable JSON
    def test_create_user_not_json(self):
        d = 'qwerty'
        self.assert400(
            self.client.post('/user/create', data=d, content_type=self.ct))

    # zero length name
    def test_create_user_zero_length(self):
        d = json.dumps(User(name=""))
        self.assert400(
            self.client.post('/user/create', data=d, content_type=self.ct))

    # name with invalid characters
    def test_create_user_invalid_characters(self):
        d = json.dumps(User(name="abc de."))
        self.assert400(
            self.client.post('/user/create', data=d, content_type=self.ct))


class TestUserControllerLoginError(BaseTestCase):

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
