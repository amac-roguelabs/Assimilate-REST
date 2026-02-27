# assimilate_client.SystemApi

All URIs are relative to *http://localhost:8080/APIV2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_system_users**](SystemApi.md#add_system_users) | **POST** /sytem/users/new | System User Add
[**get_system_properties**](SystemApi.md#get_system_properties) | **GET** /system | System Settings Get
[**get_system_users**](SystemApi.md#get_system_users) | **GET** /system/users | System Users List
[**get_system_users_current**](SystemApi.md#get_system_users_current) | **GET** /system/users/current | System User Current
[**select_system_user**](SystemApi.md#select_system_user) | **POST** /sytem/users/select/{username} | System User Select
[**set_system_properties**](SystemApi.md#set_system_properties) | **PUT** /system | System Settings Set
[**set_system_users_current**](SystemApi.md#set_system_users_current) | **PUT** /system/users/current | System User Update

# **add_system_users**
> add_system_users(body)

System User Add

Add a new User profile.

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()
body = assimilate_client.UserData() # UserData | json with new user data to add. When the username already exists, an error is returned.

try:
    # System User Add
    api_instance.add_system_users(body)
except ApiException as e:
    print("Exception when calling SystemApi->add_system_users: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserData**](UserData.md)| json with new user data to add. When the username already exists, an error is returned. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_system_properties**
> SystemData get_system_properties()

System Settings Get

Return the system settings of the Assimilate Product Suite application

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()

try:
    # System Settings Get
    api_response = api_instance.get_system_properties()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->get_system_properties: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**SystemData**](SystemData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_system_users**
> UserDataList get_system_users()

System Users List

Get the list of User profiles.

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()

try:
    # System Users List
    api_response = api_instance.get_system_users()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->get_system_users: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**UserDataList**](UserDataList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_system_users_current**
> UserData get_system_users_current()

System User Current

Get the active User profile.

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()

try:
    # System User Current
    api_response = api_instance.get_system_users_current()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->get_system_users_current: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**UserData**](UserData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **select_system_user**
> select_system_user(username)

System User Select

Activate a User profile. Returns an error when the User is not found.

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()
username = 'username_example' # str | Username of the user to select

try:
    # System User Select
    api_instance.select_system_user(username)
except ApiException as e:
    print("Exception when calling SystemApi->select_system_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**| Username of the user to select | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_system_properties**
> set_system_properties(body)

System Settings Set

Return the changed system settings of the Assimilate Product Suite application

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()
body = assimilate_client.SystemData() # SystemData | json that changes project settings

try:
    # System Settings Set
    api_instance.set_system_properties(body)
except ApiException as e:
    print("Exception when calling SystemApi->set_system_properties: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SystemData**](SystemData.md)| json that changes project settings | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_system_users_current**
> UserData set_system_users_current(body)

System User Update

Update the properties of the active User profile.

### Example
```python
from __future__ import print_function
import time
import assimilate_client
from assimilate_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assimilate_client.SystemApi()
body = assimilate_client.UserData() # UserData | json with new user data to set

try:
    # System User Update
    api_response = api_instance.set_system_users_current(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->set_system_users_current: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserData**](UserData.md)| json with new user data to set | 

### Return type

[**UserData**](UserData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

