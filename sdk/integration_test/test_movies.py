from __future__ import print_function
import time
import os
import uuid
import chiller_api_client
from chiller_api_client import User, ApiClient, Movie, MovieList
from chiller_api_client.rest import ApiException
from pprint import pprint
from chiller_api_client.configuration import Configuration

import pytest
import jwt

class TestMovieAPISuccess():

    def test_add_and_list_movies(self, user_api, movies_api):

        # create a unique username
        username = uuid.uuid4().hex
 
        # create the new user
        assert user_api.create_user(body=User(name=username)) is None
 
        # log in as user
        response = user_api.login_user(username)
        assert('token' in response.to_dict())
        token = response.to_dict()['token']
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["id"]

        # movie list
        response = movies_api.list_movies(user_id)
        assert len(response) == 0

        m1 = uuid.uuid4().hex
        # add a movie and list
        assert movies_api.add_movie(user_id, body=Movie(m1)) is None

        # movie list
        response = movies_api.list_movies(user_id)
        assert len(response) == 1

        m2 = uuid.uuid4().hex
        # add two more movies and list
        assert movies_api.add_movie(user_id, body=Movie(m1)) is None
        assert movies_api.add_movie(user_id, body=Movie(m2)) is None

        # movie list
        response = movies_api.list_movies(user_id)
        assert len(response) == 3


class TestMovieAPIFailure():

    def test_movies_list_user_doesnt_exist(self, movies_api):

        with pytest.raises(ApiException) as e:
            response = movies_api.list_movies(9999)
        assert e.value.status == 403
        print(f"response when user does not exist: {e.value}")
        print("body: {}".format(e.value.body))


    def test_movies_add_user_doesnt_exist(self, movies_api):
    # add movie user doesn't exist

        m1 = uuid.uuid4().hex
        with pytest.raises(ApiException) as e:
            movies_api.add_movie(9999, body=Movie(m1))
        assert e.value.status == 403

    def test_movies_add_bad_title(self, movies_api, user_api):

        # create a unique username
        username = uuid.uuid4().hex
        # create the new user
        assert user_api.create_user(body=User(name=username)) is None
 
        # log in as user to get user_id
        response = user_api.login_user(username)
        token = response.to_dict()['token']
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload["id"]

    # add empty title
        with pytest.raises(ApiException) as e:
            movies_api.add_movie(user_id, body=Movie(''))
        assert e.value.status == 400

    # add illegal characters title
        with pytest.raises(ApiException) as e:
            movies_api.add_movie(user_id, body=Movie('-_^'))
        assert e.value.status == 400
