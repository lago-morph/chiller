# chiller_api_client.MoviesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_movie**](MoviesApi.md#add_movie) | **POST** /movies/add/{user_id} | Add a movie to user&#x27;s list
[**list_movies**](MoviesApi.md#list_movies) | **GET** /movies/list/{user_id} | Get the list of movies for a user

# **add_movie**
> add_movie(user_id, body=body)

Add a movie to user's list

### Example
```python
from __future__ import print_function
import time
import chiller_api_client
from chiller_api_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = chiller_api_client.MoviesApi()
user_id = 56 # int | user ID
body = chiller_api_client.Movie() # Movie | Movie to add to user list (optional)

try:
    # Add a movie to user's list
    api_instance.add_movie(user_id, body=body)
except ApiException as e:
    print("Exception when calling MoviesApi->add_movie: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| user ID | 
 **body** | [**Movie**](Movie.md)| Movie to add to user list | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_movies**
> MovieList list_movies(user_id)

Get the list of movies for a user

### Example
```python
from __future__ import print_function
import time
import chiller_api_client
from chiller_api_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = chiller_api_client.MoviesApi()
user_id = 56 # int | user ID

try:
    # Get the list of movies for a user
    api_response = api_instance.list_movies(user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MoviesApi->list_movies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| user ID | 

### Return type

[**MovieList**](MovieList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

