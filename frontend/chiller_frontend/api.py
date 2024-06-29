from chiller_api_client import User, ApiClient, UserApi, MoviesApi, Movie
from chiller_api_client.rest import ApiException
from chiller_api_client.configuration import Configuration
import os

class ChillerSDK():

    def __init__(self):

        conf = Configuration()
        hostkey = "CHILLER_HOST"
        if hostkey in os.environ:
            conf.host = os.environ[hostkey]
        else:
            conf.host = '127.0.0.1:8080'
        self.u = UserApi(ApiClient(conf))
        self.m = MoviesApi(ApiClient(conf))


    def get_user_login(self, name):
        """
        call user login api
        
        returns result, message
        
        On success result is a JWT string with user information and message is ''
        On failure result is None and message is a descriptive error message
        """
        try:
            response = self.u.login_user(name)
        except ApiException as e:
            return None, e.body
    
        return response, ''
    
    def user_create(self, name):
        """
        call user create api
        
        returns result, message
        on success, result is True and message is ''
        on failure, result is False and message is descriptive error message
        """
        try:
            self.u.create_user(body=User(name))
        except ApiException as e:
            return False, e.body
    
        return True, ''
    
    def get_movies_list(self, user_id):
        """
        call movies list api
        
        returns result, message
        on success, result is a list of movie objects and message is ''
        on failure, result is None and message is descriptive error message
        """
        try:
            response = self.m.list_movies(user_id)
        except ApiException as e:
            return None, e.body
    
        return response, ''

    def movies_add(self, user_id, title):
        """
        call movies add api
        
        returns result, message
        on success, result is True and message is ''
        on failure, result is False and message is descriptive error message
        """
        try:
            self.movies_api.add_movie(user_id, body=Movie(title))
        except ApiException as e:
            return False, e.body
    
        return True, ''
    
