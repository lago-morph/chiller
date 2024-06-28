# chiller_api_client.UserApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](UserApi.md#create_user) | **POST** /user/create | Create a new user
[**login_user**](UserApi.md#login_user) | **GET** /user/login/{user_name} | Log in as user

# **create_user**
> create_user(body=body)

Create a new user

### Example
```python
from __future__ import print_function
import time
import chiller_api_client
from chiller_api_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = chiller_api_client.UserApi()
body = chiller_api_client.User() # User | User to create (optional)

try:
    # Create a new user
    api_instance.create_user(body=body)
except ApiException as e:
    print("Exception when calling UserApi->create_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**User**](User.md)| User to create | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_user**
> JWT login_user(user_name)

Log in as user

Log in as the specified user and get the authentication token

### Example
```python
from __future__ import print_function
import time
import chiller_api_client
from chiller_api_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = chiller_api_client.UserApi()
user_name = 'user_name_example' # str | Username

try:
    # Log in as user
    api_response = api_instance.login_user(user_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->login_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_name** | **str**| Username | 

### Return type

[**JWT**](JWT.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

