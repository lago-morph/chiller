import pytest
from flask import g
from flask import session
from flask import url_for

import jwt

from chiller_api_client.api.user_api import UserApi
from chiller_api_client import User, JWT
from chiller_api_client.rest import ApiException

from pprint import pprint

    
class TestLoginRedirect():

    @pytest.mark.parametrize(("call_path", "use_get"), (
                                ("/", True),
                                ("/movies/list", True),
                                ("/movies/add", False),
    ))
    def test_redirects_not_logged_in(self, client, call_path, use_get):
        with client:
            if use_get:
                r = client.get(call_path)
            else: 
                r = client.post(call_path)

            # ensure we are redirected to right place
            assert r.headers["Location"] == url_for('user.login')
        # we are redirecting from a POST to a GET.  Old way, 302.  New way 303.
        assert r.status_code == 302 or r.status_code == 303

class TestAuthFixture():

    def test_login_with_auth(self, client, auth):
        auth.login()
    
class TestGETLoginSuccess():
    # success GET login page displayed
    def test_login_get(self, client, app):
        # test that viewing the page renders without template errors
        assert client.get("/user/login").status_code == 200
    
class TestPOSTLoginSuccess():
    # success POST login with valid user
    # success POST create with valid user

    @pytest.mark.parametrize("create_first", (False,True))
    def test_login_post(self, client, app, monkeypatch, create_first):
    
        username = 'abcd'
        userid = 123
        u_obj = User(name=username, id=userid)
        key = "secret"
        encoded = jwt.encode(u_obj.to_dict(), key, algorithm="HS256")
        myjwt = JWT(token = encoded)
    
        def mock_call(a, *args, **kwargs):
            return myjwt
        def do_nothing(a, *args, **kwargs):
            pass
    
        monkeypatch.setattr(UserApi, "login_user", mock_call)
        monkeypatch.setattr(UserApi, "create_user", do_nothing)
    
        with client:
            if create_first:
                r = client.post("/user/create", data={"username": "abcd"})
            else:
                r = client.post("/user/login", data={"username": "abcd"})
            # ensure we are redirected to right place
            assert r.headers["Location"] == url_for('movies.list')
            # token has been added to session
            assert session['jwt_token'] == myjwt.to_dict()
    
        # we are redirecting from a POST to a GET.  Old way, 302.  New way 303.
        assert r.status_code == 302 or r.status_code == 303


class TestPOSTComplicatedCreateAndLoginError():

    # error POST create user successfully but login fails
    # error POST login with unregistered user 
    # error POST create user already exists
    @pytest.mark.parametrize(("call_path", "fail_func", "allow_create_first"), (
        ("/user/login", "login_user", False),  # calls login, fails login
        ("/user/create", "create_user", False), # calls create, fails create
        ("/user/create", "login_user", True), # calls create, fails login
    ))
    def test_login_post_unregistered_user(self, client, monkeypatch, call_path, fail_func, allow_create_first, auth):
    
        msg = b'a descriptive error'
        def fail_call(a, *args, **kwargs):
            e = ApiException()
            e.body = msg
            raise e
    
        monkeypatch.setattr(UserApi, fail_func, fail_call)

        if allow_create_first:
            def mock_login(*args, **kwargs):
                return auth.myjwt
            monkeypatch.setattr(UserApi, "create_user", mock_login)

    
        with client:
            response = client.post(call_path, data={"username": auth.username})
            # ensure we are redirected to right place
            assert response.headers["Location"] == url_for('user.login')
    
        # we are redirecting from a POST to a GET.  Old way, 302.  New way 303.
        assert response.status_code == 302 or response.status_code == 303

        # now have to load the redirect to check the flash error message
        redirect = response.headers["Location"]
        r2 = client.get(redirect)
        assert msg in r2.data

        # verify that the flash error goes away if I go to the page again
        r3 = client.get(redirect)
        assert msg not in r3.data

class TestPOSTLoginError():

    # error POST login missing name
    @pytest.mark.parametrize("data", (
        None, 
        {"username": None}, 
        {"username": ""}, 
        {"key": "value"} 
    ))
    def test_login_post_missing_name(self, client, data):
        r = client.post("/user/login", data=data)
        assert r.status_code == 200
        assert b'Username is required' in r.data

    # error POST login invalid name
    # this is integration testing since I don't check for this in my code.

class TestPUTLoginError():

    # error PUT login user invalid method
    def test_login_put_bad_method(self, client, app, monkeypatch):
        r = client.put("/user/login", data={"username": "abcd"})
        assert r.status_code == 405

# create
    # success POST create user
    # done as a mark parametrize in test_login_post()

class TestPOSTCreateError():
    # error POST create user missing name

    @pytest.mark.parametrize("data", (
        None, 
        {"username": None}, 
        {"username": ""}, 
        {"key": "value"} 
    ))
    def test_create_post_missing_name(self, client, data):
        with client:
            r = client.post("/user/create", data=data)
            # ensure we are redirected to right place
            redirect = r.headers["Location"]
            assert redirect == url_for('user.login')

        assert r.status_code == 302 or r.status_code == 303

        # now have to load the redirect to check the flash error message
        r2 = client.get(redirect)
        assert b'Username is required' in r2.data

    # error POST create user invalid name
    # this is integration testing since I don't check for this in my code.


    # error GET create user invalid method
    def test_create_get_bad_method(self, client):
        r = client.get("/user/create", data={"username": "abcd"})
        assert r.status_code == 405

class TestGETLogoutSuccess():
    # logout

    # success GET logout session cleared for logged in user
    def test_logout_user_logged_in(self, client, auth):
        # we have an embedded test inside the auth fixture to check that 
        # auth.login() gets a JWT with the right payload
        auth.login()
    
        with client:
            auth.logout()
            assert "my_jwt" not in session

    # success GET logout session cleared nobody logged in
    def test_logout_no_user(self, client, auth):
        with client:
            auth.logout()
            assert "my_jwt" not in session

class TestPOSTLogoutError():
    # error POST logout invalid method
    def test_logout_post_bad_method(self, client):
        r = client.post("/user/logout")
        assert r.status_code == 405

