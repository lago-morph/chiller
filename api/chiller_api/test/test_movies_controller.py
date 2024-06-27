# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from chiller_api.models.movie import Movie  # noqa: E501
from chiller_api.test import BaseTestCase

from chiller_api.db import queries


class TestMovieControllerAddSuccess(BaseTestCase):
    """/movies/add unit tests"""

    @classmethod
    def setUpClass(cls):
        cls.ct = 'application/json'
        cls.d = '{"name": "test name"}'

    def test_invalid_path(self):
        self.assert404(self.client.get('/invalid/path'))

    def test_add_movie_replicas(self):
        # add normal movie
        """Test case for add_movie

        Add a movie to user's list
        """
        # create a user
        username = "bob"
        queries.add_user(username)
        user_id = queries.get_user_id(username)
        assert user_id is not None

        body = Movie(name="test name")
        response = self.client.open(
            '/movies/add/{user_id}'.format(user_id=user_id),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 201,
                       'Response body is : ' + response.data.decode('utf-8'))

        # add another movie, should also be fine
        self.assertStatus(response, 201)

class TestMovieControllerAddError(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ct = 'application/json'
        cls.d = '{"name": "test name"}'

    def test_add_movie_empty_id(self):
        self.assert404(self.client.post('/movies/add', 
                                data=self.d, content_type=self.ct))

    def test_add_movie_string_id(self):
        self.assert404(self.client.post('/movies/add/abcd', 
                                data=self.d, content_type=self.ct))

    def test_add_movie_doesnt_exist_id(self):
        self.assert403(self.client.post('/movies/add/23', 
                                data=self.d, content_type=self.ct))

    def test_add_movie_extra_path(self):
        self.assert404(self.client.post('/movies/add/1/some/path', 
                                data=self.d, content_type=self.ct))

    def test_add_movies_wrong_method(self):
        self.assert405(self.client.get('/movies/add/1', 
                                data=self.d, content_type=self.ct))

    def test_add_movie_empty_payload(self):
        self.assert400(self.client.post('/movies/add/1'))

    def test_add_movie_wrong_payload(self):
        d = '{"somekey": 4, "otherkey": "some value"}'
        self.assert400(self.client.post('/movies/add/1', 
                                data=d, content_type=self.ct))

    def test_add_movie_empty_movie_name(self):
        d = json.dumps(Movie(""))
        self.assert400(self.client.post('/movies/add/1', 
                                data=d, content_type=self.ct))


class TestListMoviesControllerSuccess(BaseTestCase):
    """/movies/list unit tests"""

    @classmethod
    def setUpClass(cls):
        cls.ct = 'application/json'
        cls.d = '{"name": "test name"}'

    # tests getting several movies in a list with a duplicate
    def test_list_movies_mult(self):
        # create a user
        username = "bob"
        queries.add_user(username)
        user_id = queries.get_user_id(username)
        assert user_id is not None

        # add some movies
        m1 = 'sdfj3sdkjf8800sd'
        m2 = '897sdf7sdkld'
        queries.add_movie_list(user_id, json.dumps(Movie(m1)))
        queries.add_movie_list(user_id, json.dumps(Movie(m2)))
        queries.add_movie_list(user_id, json.dumps(Movie(m2)))

        response = self.client.get('/movies/list/{uid}'.format(uid=user_id))
        assert response.status_code == 200
        assert len(response.get_json()) == 3
        assert m1.encode() in response.data
        assert m2.encode() in response.data

    def test_list_movies_empty_list(self):
        # empty list from valid ID
        # create a user
        username = "bob"
        queries.add_user(username)
        user_id = queries.get_user_id(username)
        assert user_id is not None

        response = self.client.get('/movies/list/{uid}'.format(uid=user_id))
        assert response.status_code == 200
        assert len(response.get_json()) == 0

class TestListMoviesControllerError(BaseTestCase):
    """/movies/list unit tests"""

    def test_list_movies_empty_id(self):
        self.assert404(self.client.get('/movies/list'))

    def test_list_movies_string_id(self):
        self.assert404(self.client.get('/movies/list/abcd'))

    def test_list_movies_doesnt_exist_id(self):
        self.assert403(self.client.get('/movies/list/1'))

    def test_list_movies_extra_path(self):
        self.assert404(self.client.get('/movies/list/1/some/path'))

    def test_list_movies_wrong_method(self):
        self.assert405(self.client.post('/movies/list/1'))

if __name__ == '__main__':
    import unittest
    unittest.main()
