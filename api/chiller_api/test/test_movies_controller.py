# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from chiller_api.models.movie import Movie  # noqa: E501
from chiller_api.test import BaseTestCase


class TestMoviesController(BaseTestCase):
    """MoviesController integration test stubs"""

    def test_add_movie(self):
        """Test case for add_movie

        Add a movie to user's list
        """
        body = Movie()
        response = self.client.open(
            '/movies/add/{userID}'.format(user_id=56),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_movies(self):
        """Test case for list_movies

        Get the list of movies for a user
        """
        response = self.client.open(
            '/movies/list/{userID}'.format(user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
