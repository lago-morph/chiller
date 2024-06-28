from __future__ import print_function
import time
import os
import uuid
import chiller_api_client
from chiller_api_client import User, ApiClient, UserApi
from chiller_api_client.rest import ApiException
from pprint import pprint
from chiller_api_client.configuration import Configuration

import pytest

class TestUserAPISuccess():

    def test_user_login(self, user_api):

        # create a unique username
        username = uuid.uuid4().hex
        body = User(name=username) 
 
        # create the new user
        assert user_api.create_user(body=body) is None
 
        # log in as user
        response = user_api.login_user(username)
        assert('token' in response.to_dict())

class TestUserAPIFailure():

    def test_user_login_doesnt_exist(self, user_api):

        # create a unique username
        username = uuid.uuid4().hex

        # log in as user
        with pytest.raises(ApiException) as e:
            response = user_api.login_user(username)
        assert e.value.status == 403

    def test_user_login_empty_user(self, user_api):
        with pytest.raises(ApiException) as e:
            response = user_api.login_user('')
        assert e.value.status == 404

    def test_user_login_space(self, user_api):
        with pytest.raises(ApiException) as e:
            response = user_api.login_user('a b')
        assert e.value.status == 400


    def test_user_create_invalid_character(self, user_api):
        body = User(name='a-b ') 
 
        # create the new user
        with pytest.raises(ApiException) as e:
            user_api.create_user(body=body)
        assert e.value.status == 400
