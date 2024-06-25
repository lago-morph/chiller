import connexion
import six

from chiller_api.models.movie import Movie  # noqa: E501
from chiller_api.models.movie_list import MovieList  # noqa: E501
from chiller_api import util


def add_movie(user_id, body=None):  # noqa: E501
    """Add a movie to user&#x27;s list

     # noqa: E501

    :param user_id: user ID
    :type user_id: int
    :param body: Movie to add to user list
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Movie.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def list_movies(user_id):  # noqa: E501
    """Get the list of movies for a user

     # noqa: E501

    :param user_id: user ID
    :type user_id: int

    :rtype: MovieList
    """
    return 'do some magic!'
