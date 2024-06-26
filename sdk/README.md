# chiller-api-client
This is a sample application for demonstrating CI/CD using GitOps and Kubernetes.  Some useful links:  * [The Watch and Chill repository](https://github.com/lago-morph/chiller) * [Design document corresponding to this version of the API](https://github.com/lago-morph/chiller/wiki/Let's-Watch-design)

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.0.2
- Package version: 0.0.1
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import chiller_api_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import chiller_api_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import chiller_api_client
from chiller_api_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = chiller_api_client.MoviesApi(chiller_api_client.ApiClient(configuration))
user_id = 56 # int | user ID
body = chiller_api_client.Movie() # Movie | Movie to add to user list (optional)

try:
    # Add a movie to user's list
    api_instance.add_movie(user_id, body=body)
except ApiException as e:
    print("Exception when calling MoviesApi->add_movie: %s\n" % e)

# create an instance of the API class
api_instance = chiller_api_client.MoviesApi(chiller_api_client.ApiClient(configuration))
user_id = 56 # int | user ID

try:
    # Get the list of movies for a user
    api_response = api_instance.list_movies(user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MoviesApi->list_movies: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to */*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*MoviesApi* | [**add_movie**](docs/MoviesApi.md#add_movie) | **POST** /movies/add/{user_id} | Add a movie to user&#x27;s list
*MoviesApi* | [**list_movies**](docs/MoviesApi.md#list_movies) | **GET** /movies/list/{user_id} | Get the list of movies for a user
*UserApi* | [**create_user**](docs/UserApi.md#create_user) | **POST** /user/create | Create a new user
*UserApi* | [**login_user**](docs/UserApi.md#login_user) | **GET** /user/login/{user_name} | Log in as user

## Documentation For Models

 - [JWT](docs/JWT.md)
 - [Movie](docs/Movie.md)
 - [MovieList](docs/MovieList.md)
 - [User](docs/User.md)

## Documentation For Authorization

 All endpoints do not require authorization.


## Author


