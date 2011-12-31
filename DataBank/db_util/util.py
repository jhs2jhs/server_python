'''
Created on Dec 16, 2011

@author: jianhuashao
'''
import sys
import uuid


    
def get_current_function_name():
    return sys._getframe(1).f_code.co_name

def get_current_class_name(it):
    #return it.__class__.__name__
    return type(it).__name__

def get_current_module_name():
    return "world"

def get_http_param(request, key):
    if (request.POST.get(key) != None): 
        return request.POST.get(key)
    elif (request.GET.get(key) != None):
        return request.GET.get(key)
    else:
        return None
    
def new_key():
    return uuid.uuid4().hex

def new_secret():
    return uuid.uuid4().hex

def new_token():
    return uuid.uuid4().hex
