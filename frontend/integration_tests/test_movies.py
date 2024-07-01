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
    def test_get_list_success(self, client, auth, num_movies):
        auth.login(create_first = True)

        l = []
        for t in range(num_movies):
            l.append({'title': uuid.uuid4().hex})
        if num_movies > 2:
            l.append(l[0])

        for t in l:
            title = t['title']
            print(f"adding movie {title}")
            r = auth.client.post("/movies/add", data=t)
            print(r.status_code)

        r = client.get("/movies/list")
        assert r.status_code == 200
        print(r.data)
        for t in l:
            assert t['title'].encode() in r.data
        assert f"<!-- { len(l) } elements -->".encode() in r.data
        assert b"FLASH ERROR" not in r.data



class TestMoviesListError():
    pass

    # error GET list for user that does not exist in db
    # this is not possible to do through straight external testing.
    # However, it is tested as part of the integration tests in the SDK

# add
class TestMoviesAddSuccess():

    # success POST add successful
    def test_post_add_success(self, client, auth): 
  
        auth.login(create_first = True)
        with client:
            r = client.post("/movies/add", data={'title': "test title"})
            assert r.headers["Location"] == url_for('movies.list')
        assert r.status_code == 302 or r.status_code == 303
        # get movie list to ensure no flash errors posted
        r = client.get(r.headers["location"])
        assert b"FLASH ERROR" not in r.data

class TestMoviesAddError():

    # error POST add title invalid characters - handled as part of integration
    def test_post_add_invalid_characters(self, client, auth): 
  
        auth.login(create_first = True)
        with client:
            r = client.post("/movies/add", data={'title': "movie_title"})
            assert r.headers["Location"] == url_for('movies.list')
        assert r.status_code == 302 or r.status_code == 303
        # get movie list to ensure flash error is posted
        r = client.get(r.headers["location"])
        assert b"FLASH ERROR" in r.data

