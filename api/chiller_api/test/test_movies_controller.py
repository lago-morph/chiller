# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from chiller_api.models.movie import Movie  # noqa: E501
from chiller_api.test import BaseTestCase


class TestAddMovieController(BaseTestCase):
    """/movies/add unit tests"""

    @classmethod
    def setUpClass(cls):
        cls.ct = 'application/json'
        cls.d = json.dumps('{"name": "test name"}')

    def test_invalid_path(self):
        self.assert404(self.client.get('/invalid/path'))

    def test_add_movie(self):
        # add normal movie
        """Test case for add_movie

        Add a movie to user's list
        """
        body = Movie()
        body.name = "test name"
        response = self.client.open(
            '/movies/add/{user_id}'.format(user_id=56),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_movie_empty_id(self):
        self.assert404(self.client.post('/movies/add', data=self.d, content_type=self.ct))

    def test_add_movie_negative_id(self):
        self.assert404(self.client.post('/movies/add/-2', data=self.d, content_type=self.ct))

    def test_add_movie_string_id(self):
        # string ID - this should not be 404, what is it?
        self.assert404(self.client.post('/movies/add/abcd', data=self.d, content_type=self.ct))

    def test_add_movie_doesnt_exist_id(self):
        self.assert404(self.client.post('/movies/add/23242', data=self.d, content_type=self.ct))

    def test_add_movie_extra_path(self):
        self.assert404(self.client.post('/movies/add/1/some/path', data=self.d, content_type=self.ct))

    def test_add_movies_wrong_method(self):
        self.assert405(self.client.get('/movies/add/1', data=self.d, content_type=self.ct))

    def test_add_movie_empty_payload(self):
        self.assert400(self.client.post('/movies/add/1'))

    def test_add_movie_wrong_payload(self):
        d = '{"somekey": 4, "otherkey": "some value"}'
        self.assert400(self.client.post('/movies/add/1', data=d, content_type=self.ct))

    def test_add_movie_empty_movie_name(self):
        d = json.dumps(Movie(""))
        self.assert400(self.client.post('/movies/add/1', data=d, content_type=self.ct))


class TestListMoviesController(BaseTestCase):
    """/movies/list unit tests"""

    def test_list_movies_empty_list(self):
        response = self.client.post('/user/create', data=self.d, content_type=self.ct)




        # empty list from valid ID
        pass
    def test_list_movies_one_movie_list(self):
        # one movie in list
        pass

    def test_list_movies(self):
        # several movies in list
        # several movies in list with duplicate names and empty names
        """Test case for list_movies

        Get the list of movies for a user
        """
        response = self.client.open(
            '/movies/list/{user_id}'.format(user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_movies_empty_id(self):
        self.assert404(self.client.get('/movies/list'))

    def test_list_movies_negative_id(self):
        self.assert404(self.client.get('/movies/list/-2'))

    def test_list_movies_string_id(self):
        self.assert404(self.client.get('/movies/list/abcd'))

    def test_list_movies_doesnt_exist_id(self):
        self.assert404(self.client.get('/movies/list/23242'))

    def test_list_movies_extra_path(self):
        self.assert404(self.client.get('/movies/list/1/some/path'))

    def test_list_movies_wrong_method(self):
        self.assert405(self.client.post('/movies/list/1'))

if __name__ == '__main__':
    import unittest
    unittest.main()
