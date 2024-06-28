from __future__ import print_function
import os
from chiller_api_client import ApiClient, UserApi, MoviesApi
from chiller_api_client.configuration import Configuration

import pytest

@pytest.fixture
def user_api():
    conf = Configuration()
    hostkey = "CHILLER_HOST"
    if hostkey in os.environ:
        conf.host = os.environ[hostkey]
    else:
        conf.host = '127.0.0.1:8080'

    a = UserApi(ApiClient(conf))
    return a

@pytest.fixture
def movies_api():
    conf = Configuration()
    hostkey = "CHILLER_HOST"
    if hostkey in os.environ:
        conf.host = os.environ[hostkey]
    else:
        conf.host = '127.0.0.1:8080'

    a = MoviesApi(ApiClient(conf))
    return a

