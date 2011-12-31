'''
Created on Dec 16, 2011

@author: jianhuashao
'''

from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.core import serializers
import exception_db as db_except
import http_protocol_db as protocol
import json
import urllib
import ast

def get_http_param(request, key):
    if (request.POST.get(key) != None): 
        return request.POST.get(key)
    elif (request.GET.get(key) != None):
        return request.GET.get(key)
    else:
        return None
 
# need to make sure it can parse both lowercase and upcase, now it is only original   
def get_json_param(obj, key):
    value = obj.get(key)
    if (value == None):
        raise db_except.RequestParammissingError(key, obj)
    return value


def example_http_encode():
    params = {
        #'action_params': json.dumps({"source":"resource", "status": "init", "body": {"name":"source_test", "url":"http://localhost:8000:/sauth", "description":"desc_test", "callback":"http://localhost:8001/sauth", "method":"POST", "target":""}}),
        #'action_params': json.dumps({"source":"resource", "status": "request", "body":{"token_key":"1234567", "target":"", "callback":"http://localhost:8001:/sauth", "method":"post"}}),
        'action_params': json.dumps({"source":"resource", "status": "authorize", "body":{"token_key":"1234567"}}),
        'action':"register",
        }
    s = urllib.urlencode(params)
    print s

# need to use json to convert the string first and then divert it back
def parse_json_action_params(key, action_params):
    #print "parse_json_action_params"+str(action_params)
    try:
        json_object = json.loads(action_params)
        #print json_object
        if (type(json_object) != dict):
            raise db_except.HttpJsonNotDictError(key, action_params)
        return json_object
        '''print type(json_object)
        print json_object["world"]
        print "true" in json_object
        print json_object.get("true")'''
    except ValueError :
        raise db_except.HttpJsonDecodeError(key, action_params)

def parse_register_resource_init(status, body):
    name = get_json_param(body, protocol.REGISTER_RESOURCE_NAME)
    url = get_json_param(body, protocol.REGISTER_RESOURCE_URL)
    desc = get_json_param(body, protocol.REGISTER_RESOURCE_DESCRIPTION)
    callback = get_json_param(body, protocol.REGISTER_RESOURCE_CALLBACK)
    method = get_json_param(body, protocol.REGISTER_RESOURCE_METHOD)
    target = get_json_param(body, protocol.REGISTER_RESOURCE_TARGET)
    print method
    print type(target)
    
def parse_request(status, body):
    token_key = get_json_param(body, protocol.REGISTER_REQUEST_TOKEN_KEY)
    callback = get_json_param(body, protocol.REGISTER_REQUEST_CALLBACK)
    method = get_json_param(body, protocol.REGISTER_REQUEST_METHOD)
    target = get_json_param(body, protocol.REGISTER_REQUEST_TARGET)
    print token_key
    
def parse_authorize(status, body):
    token_key = get_json_param(body, protocol.REGISTER_AUTHORIZE_TOKEN_KEY)
    print token_key
    

def parse_register(source, status, body):
    #print source
    if (source == protocol.REGISTER_SOURCE_TOKEN):
        #need to extend here
        return 
    if (source == protocol.REGISTER_SOURCE_RESOURCE):
        # it is the normal process here 
        if (status == protocol.REGISTER_STATUS_INIT):   
            request_resource = parse_register_resource_init(status, body)
            return request_resource
        if (status == protocol.REGISTER_STATUS_REQUEST):
            request_request = parse_request(status, body)
            return request_request
        if (status == protocol.REGISTER_STATUS_AUTHORIZE):
            request_authorize = parse_authorize(status, body)
            return request_authorize
        raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_SOURCE_RESOURCE, status)
    raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_SOURCE, source) 


def parse_http_request(action, action_params):
    if (action == protocol.ACTION_TYPE_REGISTER):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_REGISTER, action_params)
        #print str(json_object) +"hello"
        #print example_http_encode()
        source = get_json_param(json_object, protocol.REGISTER_SOURCE)
        status = get_json_param(json_object, protocol.REGISTER_STATUS)
        body = get_json_param(json_object, protocol.REGISTER_BODY)
        return parse_register(source, status, body)
        #print type(parse_register(source, status, body))
    if (action == protocol.ACTION_TYPE_MANAGE):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_MANAGE, action_params)
    if (action == protocol.ACTION_TYPE_ACCESS):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_ACCESS, action_params)
    raise db_except.NotDjangoHttpRequestError(protocol.ACTION, action)

''' 
we will convert http request params into dict first 
so it would be easily convert 
'''
def parse_http_request_to_dict(request):
    print example_http_encode()
    if (type(request) != WSGIRequest):
        raise db_except.NotDjangoHttpRequestError("http_params", request)
        return 
    action = get_http_param(request, protocol.ACTION)
    if (action == None):
        raise db_except.RequestParammissingError(protocol.ACTION, request)
        return 
    action_params = get_http_param(request, protocol.ACTION_PARAM)
    if (action_params == None):
        raise db_except.RequestParammissingError(protocol.ACTION_PARAM, request)
        return 
    return parse_http_request(action, action_params)
    
    
if __name__ == '__main__':
    print "cool"