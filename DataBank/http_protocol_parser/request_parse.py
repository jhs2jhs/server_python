'''
Created on Dec 16, 2011

@author: jianhuashao
'''

from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.core import serializers
import exception as db_except
import protocol_consts as protocol
import json
import urllib
import ast
import db_util.util as db_util
 
# need to make sure it can parse both lowercase and upcase, now it is only original   
def get_json_param(obj, key):
    value = obj.get(key)
    if (value == None):
        raise db_except.RequestParammissingError(key, obj)
    return value


def example_http_encode():
    params = {
        'action_params': json.dumps({"source":"resource", "status": "init", "body": {"name":"source_test", "url":"http://localhost:8000:/sauth", "description":"desc_test", "callback":"http://localhost:8001/sauth", "method":"POST", "target":""}}),
        #'action_params': json.dumps({"source":"resource", "status": "request", "body":{"token_key":"1234567", "target":"", "callback":"http://localhost:8001:/sauth", "method":"post"}}),
        #'action_params': json.dumps({"source":"resource", "status": "authorize", "body":{"token_key":"1234567"}}),
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

def parse_register_token_init(myparser, status, body):
    token_key = get_json_param(body, protocol.REGISTER_AUTHORIZE_TOKEN_KEY)
    return myparser().register_token_init(token_key)

def parse_register_resource_init(myparser, status, body):
    name = get_json_param(body, protocol.REGISTER_RESOURCE_NAME)
    url = get_json_param(body, protocol.REGISTER_RESOURCE_URL)
    desc = get_json_param(body, protocol.REGISTER_RESOURCE_DESCRIPTION)
    callback = get_json_param(body, protocol.REGISTER_RESOURCE_CALLBACK)
    method = get_json_param(body, protocol.REGISTER_RESOURCE_METHOD)
    target = get_json_param(body, protocol.REGISTER_RESOURCE_TARGET)
    return myparser().register_resource_init(name, url, desc, callback, method, target)
    
def parse_register_request(myparser, status, body):
    token_key = get_json_param(body, protocol.REGISTER_REQUEST_TOKEN_KEY)
    callback = get_json_param(body, protocol.REGISTER_REQUEST_CALLBACK)
    method = get_json_param(body, protocol.REGISTER_REQUEST_METHOD)
    target = get_json_param(body, protocol.REGISTER_REQUEST_TARGET)
    return myparser().register_request(token_key, callback, method, target)
    
def parse_register_authorize(myparser, status, body):
    token_key = get_json_param(body, protocol.REGISTER_AUTHORIZE_TOKEN_KEY)
    return myparser().register_authorize(token_key)
    

def parse_register(myparser, source, status, body):
    #print source
    if (source == protocol.REGISTER_SOURCE_TOKEN):
        #need to extend here
        if (status == protocol.REGISTER_STATUS_INIT):   
            register_resource = parse_register_token_init(myparser, status, body)
            return register_resource
        if (status == protocol.REGISTER_STATUS_REQUEST):
            register_request = parse_register_request(myparser, status, body)
            return register_request
        if (status == protocol.REGISTER_STATUS_AUTHORIZE):
            register_authorize = parse_register_authorize(myparser, status, body)
            return register_authorize
        raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_SOURCE_RESOURCE, status)
    if (source == protocol.REGISTER_SOURCE_RESOURCE):
        # it is the normal process here 
        if (status == protocol.REGISTER_STATUS_INIT):   
            register_resource = parse_register_resource_init(myparser, status, body)
            return register_resource
        if (status == protocol.REGISTER_STATUS_REQUEST):
            register_request = parse_register_request(myparser, status, body)
            return register_request
        if (status == protocol.REGISTER_STATUS_AUTHORIZE):
            register_authorize = parse_register_authorize(myparser, status, body)
            return register_authorize
        raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_SOURCE_RESOURCE, status)
    raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_SOURCE, source) 


def parse_manage(myparser, operation, body, token_key, callback, method, target):
    if (operation == protocol.MANAGE_OPERATION_METADATA):
        return myparser.manage_metadata(body, token_key, callback, method, target)
    if (operation == protocol.MANAGE_OPERATION_SETTING):
        return myparser.manage_setting(body, token_key, callback, method, target)
    if (operation == protocol.MANAGE_OPERATION_BILL):
        return myparser.manage_bill(body, token_key, callback, method, target)
    if (operation == protocol.MANAGE_OPERATION_FEEDBACK):
        return myparser.manage_feedback(body, token_key, callback, method, target)
    if (operation == protocol.MANAGE_OPERATION_INQUIRY):
        return myparser.manage_inquiry(body, token_key, callback, method, target)
    raise db_except.NotDjangoHttpRequestError(protocol.MANAGE_OPERATION, operation) 


def parse_access(myparser, body, token_key, callback, method, target):
    access_token_key = get_json_param(body, protocol.ACCESS_BODY_TOKEN_KEY)
    timestamp = get_json_param(body, protocol.ACCESS_BODY_TIMESTAMP)
    return myparser.access(access_token_key, timestamp, token_key, callback, method, target)

def parse_http_request(myparser, action, action_params):
    if (action == protocol.ACTION_TYPE_REGISTER):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_REGISTER, action_params)
        #print str(json_object) +"hello"
        #print example_http_encode()
        source = get_json_param(json_object, protocol.REGISTER_SOURCE)
        status = get_json_param(json_object, protocol.REGISTER_STATUS)
        body = get_json_param(json_object, protocol.REGISTER_BODY)
        return parse_register(myparser, source, status, body)
        #print type(parse_register(source, status, body))
    if (action == protocol.ACTION_TYPE_MANAGE):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_MANAGE, action_params)
        operation = get_json_param(json_object, protocol.MANAGE_OPERATION)
        body = get_json_param(json_object, protocol.MANAGE_BODY)
        token_key = get_json_param(json_object, protocol.MANAGE_TOKEN_KEY)
        callback = get_json_param(json_object, protocol.MANAGE_CALLBACK)
        method = get_json_param(json_object, protocol.MANAGE_METHOD)
        target = get_json_param(json_object, protocol.MANAGE_TARGET)
        return parse_manage(myparser, operation, body, token_key, callback, method, target)
    if (action == protocol.ACTION_TYPE_ACCESS):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_ACCESS, action_params)
        body = get_json_param(json_object, protocol.ACCESS_BODY)
        token_key = get_json_param(json_object, protocol.ACCESS_TOKEN_KEY)
        callback = get_json_param(json_object, protocol.ACCESS_CALLBACK)
        method = get_json_param(json_object, protocol.ACCESS_METHOD)
        target = get_json_param(json_object, protocol.ACCESS_TARGET)
        return parse_access(myparser, body, token_key, callback, method, target)
    raise db_except.NotDjangoHttpRequestError(protocol.ACTION, action)

''' 
    we will convert http request params into dict first 
    so it would be easily convert 
'''
def parse_http_request_to_dict(myparser, request):
    #print example_http_encode()
    if (type(request) != WSGIRequest):
        raise db_except.NotDjangoHttpRequestError("http_params", request)
        return 
    action = db_util.get_http_param(request, protocol.ACTION)
    if (action == None):
        raise db_except.RequestParammissingError(protocol.ACTION, request)
        return 
    action_params = db_util.get_http_param(request, protocol.ACTION_PARAM)
    if (action_params == None):
        raise db_except.RequestParammissingError(protocol.ACTION_PARAM, request)
        return 
    return parse_http_request(myparser, action, action_params)
    
    
if __name__ == '__main__':
    print "cool"