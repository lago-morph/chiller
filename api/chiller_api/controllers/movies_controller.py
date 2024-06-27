import connexion
import six
import string

from chiller_api.models.movie import Movie  # noqa: E501
from chiller_api.models.movie_list import MovieList  # noqa: E501
from chiller_api import util

from chiller_api.db import queries


def add_movie(user_id, body=None):  # noqa: E501
    """Add a movie to user&#x27;s list
    """

    if connexion.request.is_json:
        body = Movie.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return 'no JSON object in request', 400

    # maybe this is done by connexion automatically as it is marked as 
    # required in the .yaml file
    if user_id is None:
        return 'user_id not specified', 400

    if body.name is None:
        return 'name key not set in JSON object', 400

    if len(body.name) == 0:
        return 'zero length name in JSON object', 400

    allowed = set(string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits + ' ' + ':')
    if not (set(body.name) <= allowed):
        return 'name can only have alphabetic characters, digits, space, and colon', 400

    if queries.add_movie_list(user_id,body.name):
        return 'movie added', 201
    else:
        return 'user ID not found', 403



def list_movies(user_id):  # noqa: E501
    """Get the list of movies for a user

     # noqa: E501

    :param user_id: user ID
    :type user_id: int

    :rtype: MovieList
    """


    # required in the .yaml file
    if user_id is None:
        return 'user_id not specified', 400

    # validate the user_id exists in the database
    if queries.get_user_name(user_id) is None:
        return 'user ID not found', 403

    # I can't figure out for the life of me how to use the generated
    # MovieList class.  Ugh.

    # get the movies in this users list
    movies = queries.get_movielist(user_id)
    print(movies)
    ml = []
    if movies is not None:
        for movie in movies:
            ml.append({"name": movie[0]})

    return ml, 200



