# swagger_client.CommentsApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**comments_create**](CommentsApi.md#comments_create) | **POST** /comments |
[**comments_delete**](CommentsApi.md#comments_delete) | **DELETE** /comments/{id} | Method removes a comment from an issue
[**comments_partial_update**](CommentsApi.md#comments_partial_update) | **PATCH** /comments/{id} | Method updates comment in an issue


# **comments_create**
> Comment comments_create(data)





### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CommentsApi(swagger_client.ApiClient(configuration))
data = swagger_client.Comment() # Comment |

try:
    api_response = api_instance.comments_create(data)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CommentsApi->comments_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**Comment**](Comment.md)|  |

### Return type

[**Comment**](Comment.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **comments_delete**
> comments_delete(id)

Method removes a comment from an issue



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CommentsApi(swagger_client.ApiClient(configuration))
id = 56 # int | A unique integer value identifying this comment.

try:
    # Method removes a comment from an issue
    api_instance.comments_delete(id)
except ApiException as e:
    print("Exception when calling CommentsApi->comments_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this comment. |

### Return type

void (empty response body)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **comments_partial_update**
> Comment comments_partial_update(id, data)

Method updates comment in an issue



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: Basic
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CommentsApi(swagger_client.ApiClient(configuration))
id = 56 # int | A unique integer value identifying this comment.
data = swagger_client.Comment() # Comment |

try:
    # Method updates comment in an issue
    api_response = api_instance.comments_partial_update(id, data)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CommentsApi->comments_partial_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this comment. |
 **data** | [**Comment**](Comment.md)|  |

### Return type

[**Comment**](Comment.md)

### Authorization

[Basic](../README.md#Basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
