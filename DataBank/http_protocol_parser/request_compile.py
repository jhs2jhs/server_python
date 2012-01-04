'''
Created on Jan 4, 2012

@author: jianhuashao
'''
import protocol_consts as protocol

class request_compile_base:
    def __init__(self):
        '''it is a base class for all request process'''
    def get_register(self, register_status=protocol.REGISTER_STATUS_INIT, register_body):
        register = {
            protocol.REGISTER_STATUS:register_status,
            protocol.REGISTER_BODY: register_body,
            }
        return register
    def get_access(self, access_type=protocol.ACCESS_TYPE_1, access_body):
        access = {
            protocol.ACCESS_TYPE: access_type, 
            protocol.ACCESS_BODY: access_body, 
            }
        return access

def get_register_object_init(
        object_type = protocol.REGISTER_INIT_OBJECT_TYPE_RESOURCE, 
        object_resource, 
        object_token = None, 
        object_name, 
        object_alias, 
        object_permission = protocol.REGISTER_INIT_OBJECT_PERMISSION_MANAGE, 
        object_description):
    object_init = {
        protocol.REGISTER_INIT_OBJECT_TYPE : object_type,
        protocol.REGISTER_INIT_OBJECT_RESOURCE : object_resource,
        protocol.REGISTER_INIT_OBJECT_TOKEN : object_token,
        protocol.REGISTER_INIT_OBJECT_NAME : object_name,
        protocol.REGISTER_INIT_OBJECT_ALIAS : object_alias,
        protocol.REGISTER_INIT_OBJECT_PERMISSION : object_permission,
        protocol.REGISTER_INIT_OBJECT_DESCRIPTION : object_description,
        }
    register_status = protocol.REGISTER_STATUS_INIT
    register_body = object_init
    return request_compile_base().get_register(register_status, register_body)
def get_register_request(
        request_source, 
        request_target, 
        request_operation = protocol.REGISTER_REQUEST_OPERATION_MANAGE, 
        request_status = protocol.REGISTER_REQUEST_STATUS_REQUEST):
    register_request = {
        protocol.REGISTER_REQUEST_SOURCE : request_source,
        protocol.REGISTER_REQUEST_TARGET : request_target,
        protocol.REGISTER_REQUEST_OPERATION : request_operation,
        protocol.REGISTER_REQUEST_STATUS : request_status,
        }
    register_status = protocol.REGISTER_STATUS_REQUEST
    register_body = register_request
    return request_compile_base().get_register(register_status, register_body)

def get_register_authorize(authorize_token):
    register_authorize = {
        protocol.REGISTER_AUTHORIZE_TOKEN_KEY : authorize_token,
        }
    register_status = protocol.REGISTER_STATUS_AUTHORIZE
    register_body = register_authorize
    return request_compile_base().get_register(register_status, register_body)
    
def request_compile_register():
    object_type = protocol.REGISTER_INIT_OBJECT_TYPE_RESOURCE
    object_resource = "hello"
    object_token = "hello"
    object_name = "hello"
    object_alias = "hello"
    object_permission = protocol.REGISTER_INIT_OBJECT_PERMISSION_MANAGE
    object_description = "hello"
    object_init = get_register_object_init(object_type, object_resource, object_token, 
                             object_name, object_alias, object_permission,object_description)
    
    request_source = "hello"
    request_target = "hello"
    request_operation = protocol.REGISTER_REQUEST_OPERATION_MANAGE
    request_status = protocol.REGISTER_REQUEST_STATUS_REQUEST
    register_request = get_register_request(request_source, request_target, request_operation, request_status)
    
    authorize_token = "hello"
    register_authorize = get_register_authorize(authorize_token) 
    
    return register_authorize


def request_compile_manage():
    '''hello world'''
    
def get_access_1(
        token_key, 
        query, 
        validation, 
        capability):
    access_1 = {
        protocol.ACCESS_TOKEN:token_key,
        protocol.ACCESS_QUERY:query,
        protocol.ACCESS_VALIDATION:validation,
        protocol.ACCESS_CAPABILITY:capability,
        }
    access_type = protocol.ACCESS_TYPE_1
    access_body = access_1
    return request_compile_base().get_access(access_type, access_body)

def get_access_2(
        token_key, 
        access_token_key, 
        validation, 
        query, 
        data):
    access_2 = {
        protocol.ACCESS_TOKEN:token_key,
        protocol.ACCESS_ACCESS_TOKEN:access_token_key,
        protocol.ACCESS_VALIDATION:validation,
        protocol.ACCESS_QUERY:query,
        protocol.ACCESS_BODY_DATA:data,
        }
    access_type = protocol.ACCESS_TYPE_2
    access_body = access_2
    return request_compile_base().get_access(access_type, access_body)

def get_access_3(
        access_token_key, 
        access_result):
    access_3 = {
        protocol.ACCESS_ACCESS_TOKEN:access_token_key,
        protocol.ACCESS_RESULT:access_result,
        }
    access_type = protocol.ACCESS_TYPE_3
    access_body = access_3
    return request_compile_base().get_access(access_type, access_body)
    
    
def request_compile_access():
    token_key = "hello"
    query = "hello"
    validation = "1000" # timestamp
    capability = "1000" # biggest segement
    access_1 = get_access_1(token_key, query, validation, capability)
    
    token_key = "hello"
    access_token_key = "hello"
    validation = "1000" # timestamp
    query = "hello"
    data = {"hello":"world"}
    access_2 = get_access_2(token_key, access_token_key, validation, query, data)
    
    access_token_key = "hello"
    access_result = {"hello":"world"}
    access_3 = get_access_3(access_token_key, access_result)
    
    return access_1
    
    
    
    
    