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
    
def parse_register_init_resource(myparser, resource, name, alias, permission, description, callback):
    return myparser().register_init_resource(resource, name, alias, permission, description, callback)
def parse_register_init_token(myparser, token, name, alias, permission, description, callback):
    return myparser().register_init_token(token, name, alias, permission, description, callback)

def parse_register_init(myparser, body, callback):
    type = get_json_param(body, protocol.REGISTER_INIT_OBJECT_TYPE)
    if (type == protocol.REGISTER_INIT_OBJECT_TYPE_RESOURCE):
        resource = get_json_param(body, protocol.REGISTER_INIT_OBJECT_RESOURCE)
        name = get_json_param(body, protocol.REGISTER_INIT_OBJECT_NAME)
        alias = get_json_param(body, protocol.REGISTER_INIT_OBJECT_ALIAS)
        permission = get_json_param(body, protocol.REGISTER_INIT_OBJECT_PERMISSION)
        description = get_json_param(body, protocol.REGISTER_INIT_OBJECT_DESCRIPTION)
        return parse_register_init_resource(myparser, resource, name, alias, permission, description, callback)
    if (type == protocol.REGISTER_INIT_OBJECT_TYPE_TOKEN):
        token_key = get_json_param(body, protocol.REGISTER_INIT_OBJECT_TOKEN)
        name = get_json_param(body, protocol.REGISTER_INIT_OBJECT_NAME)
        alias = get_json_param(body, protocol.REGISTER_INIT_OBJECT_ALIAS)
        permission = get_json_param(body, protocol.REGISTER_INIT_OBJECT_PERMISSION)
        description = get_json_param(body, protocol.REGISTER_INIT_OBJECT_DESCRIPTION)
        return parse_register_init_token(myparser, token_key, name, alias, permission, description, callback)
    raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_INIT_OBJECT_TYPE, type)
    
def parse_register_request(myparser, status, body):
    source = get_json_param(body, protocol.REGISTER_REQUEST_SOURCE)
    target = get_json_param(body, protocol.REGISTER_REQUEST_TARGET)
    operation = get_json_param(body, protocol.REGISTER_REQUEST_OPERATION)
    status = get_json_param(body, protocol.REGISTER_REQUEST_STATUS)
    return myparser().register_request(source, target, operation, status)
    
def parse_register_authorize(myparser, status, body):
    token_key = get_json_param(body, protocol.REGISTER_AUTHORIZE_TOKEN_KEY)
    return myparser().register_authorize(token_key)
    

def parse_register(myparser, status, body, callback):
    #print source
    if (status == protocol.REGISTER_STATUS_INIT):   
        register_resource = parse_register_init(myparser, body, callback)
        return register_resource
    if (status == protocol.REGISTER_STATUS_REQUEST):
        register_request = parse_register_request(myparser, body, callback)
        return register_request
    if (status == protocol.REGISTER_STATUS_AUTHORIZE):
        register_authorize = parse_register_authorize(myparser, body, callback)
        return register_authorize
    raise db_except.NotDjangoHttpRequestError(protocol.REGISTER_SOURCE_RESOURCE, status)


def parse_manage(myparser, operation, body, token_key, callback):
    if (operation == protocol.MANAGE_OPERATION_METADATA):
        return myparser.manage_metadata(body, token_key, callback)
    if (operation == protocol.MANAGE_OPERATION_SETTING):
        return myparser.manage_setting(body, token_key, callback)
    if (operation == protocol.MANAGE_OPERATION_BILL):
        return myparser.manage_bill(body, token_key, callback)
    if (operation == protocol.MANAGE_OPERATION_FEEDBACK):
        return myparser.manage_feedback(body, token_key, callback)
    if (operation == protocol.MANAGE_OPERATION_INQUIRY):
        return myparser.manage_inquiry(body, token_key, callback)
    raise db_except.NotDjangoHttpRequestError(protocol.MANAGE_OPERATION, operation) 


def parse_access_type_1(myparser, token_key, query, validation, capability):
    return myparser().access_type_1(token_key, query, validation, capability)
def parse_access_type_2(myparser, token_key, access_token_key, validation, query, data):
    return myparser().access_type_2(token_key, access_token_key, validation, query, data)
def parse_access_type_3(myparser, access_token_key, access_result):
    return myparser().access_type_3(access_token_key, access_result)

def parse_access(myparser, type, body, callback):
    if (type == protocol.ACCESS_TYPE_1):
        token_key = get_json_param(body, protocol.ACCESS_TOKEN)
        query = get_json_param(body, protocol.ACCESS_QUERY)
        validation = get_json_param(body, protocol.ACCESS_VALIDATION)
        capability = get_json_param(body, protocol.ACCESS_CAPABILITY)
        return parse_access_type_1(myparser, token_key, query, validation, capability)
    if (type == protocol.ACCESS_TYPE_2):
        token_key = get_json_param(body, protocol.ACCESS_TOKEN)
        validation = get_json_param(body, protocol.ACCESS_VALIDATION)
        access_token_key = get_json_param(body, protocol.ACCESS_ACCESS_TOKEN)
        query = get_json_param(body, protocol.ACCESS_QUERY)
        data = get_json_param(body, protocol.ACCESS_BODY_DATA)
        return parse_access_type_2(myparser, token_key, access_token_key, validation, query, data)
    if (type == protocol.ACCESS_TYPE_3):
        access_token_key = get_json_param(body, protocol.ACCESS_ACCESS_TOKEN)
        access_result = get_json_param(body, protocol.ACCESS_RESULT)
        return parse_access_type_3(myparser, access_token_key, access_result)
    raise db_except.NotDjangoHttpRequestError(protocol.ACCESS_TYPE, type) 

def parse_http_request(myparser, action, action_params, callback):
    if (action == protocol.ACTION_TYPE_REGISTER):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_REGISTER, action_params)
        #print str(json_object) +"hello"
        #print example_http_encode()
        status = get_json_param(json_object, protocol.REGISTER_STATUS)
        body = get_json_param(json_object, protocol.REGISTER_BODY)
        return parse_register(myparser, status, body, callback)
        #print type(parse_register(source, status, body))
    if (action == protocol.ACTION_TYPE_MANAGE):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_MANAGE, action_params)
        operation = get_json_param(json_object, protocol.MANAGE_OPERATION)
        body = get_json_param(json_object, protocol.MANAGE_BODY)
        token_key = get_json_param(json_object, protocol.MANAGE_TOKEN_KEY)
        return parse_manage(myparser, operation, body, token_key, callback)
    if (action == protocol.ACTION_TYPE_ACCESS):
        json_object = parse_json_action_params(protocol.ACTION_TYPE_ACCESS, action_params)
        type = get_json_param(json_object, protocol.ACCESS_TYPE)
        body = get_json_param(json_object, protocol.ACCESS_BODY)
        return parse_access(myparser, type, body, callback)
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
    callback = db_util.get_http_param(request, protocol.CALLBACK)
    return parse_http_request(myparser, action, action_params, callback)
    
    
if __name__ == '__main__':
    print "cool"