import pytest
from flask import g
from flask import session
from flask import url_for

import jwt

from chiller_api_client.api.user_api import UserApi
from chiller_api_client import User, JWT
from chiller_api_client.rest import ApiException

from pprint import pprint

    
class TestPOSTCreateAndPOSTLoginSuccess():

    def test_login_with_auth(self, client, auth):
        r = auth.login(create_first = True)
        assert r.status_code == 302 or r.status_code == 303
        assert auth.userid is not None
        assert r.headers["Location"] == '/movies/list'
    
class TestGETLoginSuccess():
    # success GET login page displayed
    def test_login_get(self, client, app):
        # test that viewing the page renders without template errors
        assert client.get("/user/login").status_code == 200
    
class TestPOSTComplicatedCreateAndLoginError():

    # error POST create user already exists
    def create_duplicate(self, auth):
        auth.login(create_first = True)
        auth.logout()
        auth.login(create_first = True)
        assert auth.userid is None

class TestPOSTLoginError():

    # error POST login with unregistered user 
    def login_unregistered(self, auth):
        auth.login(create_first = False)
        assert auth.userid is None

    # error POST login user invalid name
    # error POST create user invalid name
    @pytest.mark.parametrize("create_first", (True, False))
    def test_create_login_with_invalid_name(self, client, auth, create_first):
        auth.username = 'user_name'
        r = auth.login(create_first = create_first)
        assert auth.userid is None
        # we redirect back to login for both failed create and login
        assert r.status_code == 302 or r.status_code == 303
        assert r.headers["Location"] == "/user/login"
        # we have to get the login page to be able to see the error
        r = client.get(r.headers['Location'])

        # get flash error and check content
        assert b'name can only have alphabetic characters and digits' in r.data

class TestGETLogoutSuccess():
    # logout

    # success GET logout session cleared for logged in user
    def test_logout_user_logged_in(self, client, auth):
        auth.login(create_first = True)
        assert auth.userid is not None
    
        with client:
            auth.logout()
            assert "my_jwt" not in session

    # success GET logout session cleared nobody logged in
    def test_logout_no_user(self, client, auth):
        with client:
            auth.logout()
            assert "my_jwt" not in session

class TestSequences():
    def test_create_logout_login(self, auth, client):
        auth.login(create_first = True)
        with client:
            auth.logout()
            assert "my_jwt" not in session
            assert auth.userid is None

        auth.login(create_first = False)
        assert auth.userid is not None
