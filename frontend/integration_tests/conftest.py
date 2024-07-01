import os
import tempfile
from chiller_api_client import User, JWT, UserApi
import jwt
import uuid
from flask import session

import pytest
from pprint import pprint

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
    def __init__(self, client):
        self.client = client
        self.username = uuid.uuid4().hex
        self.userid = None

    def login(self, username=None, create_first=False):

        if username is None:
            username = self.username

        # create is just a login that creates the user first, then calls login
        # on success, they return exactly the same thing

        if create_first:
            path = "/user/create"
        else:
            path = "/user/login"

        with self.client:
            response = self.client.post( path, data={"username": username})
            print('-------------------------------------------------------')
            pprint(session)
            print('-------------------------------------------------------')
            if 'jwt_token' in session:
                self.userid = jwt.decode(session['jwt_token']['token'], options={"verify_signature": False})

        return response

    def logout(self):
        self.userid = None
        return self.client.get("/user/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
