# coding: utf-8

from __future__ import absolute_import

from flask import json, current_app
from six import BytesIO

from chiller_api.models.jwt import JWT  # noqa: E501
from chiller_api.models.user import User  # noqa: E501
from chiller_api.test import BaseTestCase

from chiller_api.db import queries

import jwt

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
        self.assertStatus(response, 201,
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


class TestUserControllerLoginSuccess(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ct = 'application/json'

    def test_login_user(self):
        name = "bob"
        queries.add_user(name)
        response = self.client.get('/user/login/{name}'.format(name=name))

        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert "token" in data
        payload = jwt.decode(data["token"], options={"verify_signature": False})
        assert payload is not None
        assert "name" in payload
        assert payload["name"] == name
        assert "id" in payload
        assert payload["id"] is not None

class TestUserControllerLoginError(BaseTestCase):

    def test_login_user_empty(self):
        self.assert404(self.client.get('/user/login'))
        self.assert404(self.client.get('/user/login/'))
        self.assert404(self.client.get('/user/login//'))
    
    # name with invalid characters
    def test_login_user_invalid_characters(self):
        self.assert400(self.client.get(
                    '/user/login/{name}'.format(name=' ')))
        self.assert400(self.client.get(
                    '/user/login/{name}'.format(name='abc.de ')))
        self.assert400(self.client.get(
                    '/user/login/{name}'.format(name='!<>a--bc:de')))
        self.assert404(self.client.get(
                    '/user/login/{name}/'.format(name='!<>a--bc:de')))

    def test_login_user_doesnt_exist(self):
        self.assert403(self.client.get('/user/login/bob'))
        self.assert404(self.client.get('/user/login/bob/'))

    def test_login_user_wrong_method(self):
        self.assert405(self.client.post('/user/login/bob'))
        self.assert404(self.client.post('/user/login/bob/'))


if __name__ == '__main__':
    import unittest
    unittest.main()
