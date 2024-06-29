import os
import tempfile
from chiller_api_client import User, JWT, UserApi
import jwt
from flask import session

import pytest

from chiller_frontend import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test

    # create the app with common test config
    app = create_app({"TESTING": True})

    yield app

    pass


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client, monkeypatch):
        self.client = client
        self.monkeypatch = monkeypatch
        self.username = 'test'
        self.userid = 123
        self.u_obj = User(name=self.username, id=self.userid)
        self.encoded = jwt.encode(self.u_obj.to_dict(), 
                                    'notsecret', algorithm="HS256")
        self.myjwt = JWT(token = self.encoded)

    def login(self, username="test", password="test"):
        def mock_login(a, b, **kwargs):
            return self.myjwt.to_dict()

        self.monkeypatch.setattr(UserApi, "login_user", mock_login)

        with self.client:
            response = self.client.post(
                "/user/login", data={"username": self.username}
            )
            assert response.status_code == 302 or response.status_code == 303

            # it is hard to write a test case to test this fixture to make
            # sure that the token is returned.  So I'm doing it here.
            assert 'jwt_token' in session 
            assert session['jwt_token'] == self.myjwt.to_dict()

        return response

    def logout(self):
        return self.client.get("/user/logout")


@pytest.fixture
def auth(client, monkeypatch):
    return AuthActions(client, monkeypatch)
