import pytest
from flask import g
from flask import session
from flask import url_for

import jwt
import uuid

from chiller_api_client.api.movies_api import MoviesApi
from chiller_api_client import Movie
from chiller_api_client.rest import ApiException

from pprint import pprint

# list
class TestMoviesListSuccess():
    # success GET list empty list
    # success GET list one movie
    # success GET list multiple movies with duplicates
    @pytest.mark.parametrize("num_movies", (0,1,3))
    def test_get_list_success(self, client, auth, monkeypatch,num_movies):
        auth.login()

        l = []
        for t in range(num_movies):
            l.append({'title': uuid.uuid4().hex})
        if num_movies > 2:
            l.append(l[0])

        def return_movies(a, *args, **kwargs):
            return l

        monkeypatch.setattr(MoviesApi, "list_movies", return_movies)
        r = client.get("/movies/list")
        assert r.status_code == 200
        for t in l:
            assert t['title'].encode() in r.data
        assert f"<!-- { len(l) } elements -->".encode() in r.data



class TestMoviesListError():
    pass
    # error GET list user not logged in - handled in test_user.TestLoginRedirect

    # error GET list user logged in but does not exist in db
    # this is equivalent to having the list_movies api return an error when the
    # user is logged in already.  Just make sure this is handled properly
    def test_list_logged_in_but_error(self, client, auth, monkeypatch):
        msg = b'a descriptive error'
        def fail_call(a, *args, **kwargs):
            e = ApiException()
            e.body = msg
            raise e
        monkeypatch.setattr(MoviesApi, "list_movies", fail_call)
        auth.login()
        r = client.get("/movies/list")
        assert r.status_code == 200
        assert msg in r.data

    # error POST list wrong method
    def test_list_wrong_method(self, client, auth):
        auth.login()
        r = client.post("/movies/list")
        assert r.status_code == 405

# add
class TestMoviesAddSuccess():

    # success POST add successful
    def test_post_add_success(self, client, auth, monkeypatch): 
        def do_nothing(a, *args, **kwargs):
            pass
        monkeypatch.setattr(MoviesApi, "add_movie", do_nothing)
  
        auth.login()
        with client:
            r = client.post("/movies/add", data=Movie("test title").to_dict())
            assert r.headers["Location"] == url_for('movies.list')
        assert r.status_code == 302 or r.status_code == 303

class TestMoviesAddError():

    # error POST add title empty
    @pytest.mark.parametrize("data", (
        None, 
        {"title": None}, 
        {"title": ""}, 
        {"key": "value"} 
    ))
    def test_add_missing_title(self, client, data, auth):
        auth.login()
        with client:
            r = client.post("/movies/add", data=data)
            assert r.headers["Location"] == url_for('movies.list')
    
        # we are redirecting from a POST to a GET.  Old way, 302.  New way 303.
        assert r.status_code == 302 or r.status_code == 303

        # now have to load the redirect to check the flash error message
        redirect = r.headers["Location"]
        r2 = client.get(redirect)
        assert b"Movie title is required" in r2.data


    # error POST add title invalid characters - handled as part of integration

    # error POST add user not logged in - handled in test_user.TestLoginRedirect

    # error GET add wrong method
    def test_add_wrong_method(self, client, auth):
        auth.login()
        r = client.get("/movies/add")
        assert r.status_code == 405
