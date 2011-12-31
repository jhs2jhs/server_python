'''
Created on Dec 16, 2011

@author: jianhuashao
'''

import db_util.util as db_util

def print_except(msg, key, value):
    print "## Except: ##"
    print "## "+ str(msg) 
    print "## "+ str(key) + " = " + str(value)

class TestError(Exception):
    def __init__(self):
        self.hello="hello"

class Error(Exception):
    ''' base class for exceptions in this module. '''
    pass

class NotDjangoHttpRequestError(Error):
    def __init__(self, key, value):
        self.msg = "it is not a validate Django HttpRequest"
        self.key = key
        self.value = value
        print_except(self.msg, self.key, self.value)
        
class RequestParammissingError(Error):
    def __init__(self, key, value):
        self.msg = "Param '"+ key +"' is missing in request"
        self.key = key
        self.value = value
        print_except(self.msg, self.key, self.value)
        
class HttpJsonDecodeError(Error):
    def __init__(self, key, value):
        self.msg = "action_param '"+ key +"' can not decode in JSON"
        self.key = key
        self.value = value
        print_except(self.msg, self.key, self.value)
        
class HttpJsonNotDictError(Error):
    def __init__(self, key, value):
        self.msg = "Http Request '"+ key +"' can not decode from JSON into python dict object"
        self.key = key
        self.value = value
        print_except(self.msg, self.key, self.value)
        
        
