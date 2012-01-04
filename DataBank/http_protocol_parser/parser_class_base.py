'''
Created on Dec 20, 2011

@author: jianhuashao
'''

import db_util.util as db_util

def db_base_not_implement(methodname):
    msg = "## Method "+str(methodname)+" is not implemented in subclass ##"
    print msg
    print "## ===== So it uses same method but from base class =========##"
    raise NotImplementedError(msg)


# a lot of difficult need to implemnt, how to represent the object orientited programming
class HttpRequestParserBase(object):
    '''parse the http request of DataBank'''
    def __init__(self):
        pass
    
    ''' register '''
    def register_init_resource(self, resource, name, alias, permission, description, callback):
        db_base_not_implement(db_util.get_current_function_name())  
    def register_init_token(self, token_key, name, alias, permission, description, callback):
        db_base_not_implement(db_util.get_current_function_name())  
    #def register_token_init(self, token_key):
    #    db_base_not_implement(db_util.get_current_function_name())  
    #def register_resource_init(self, name, url, desc, callback, method, target):
    #    db_base_not_implement(db_util.get_current_function_name())
    def register_request(self, source, target, operation, status):
        db_base_not_implement(db_util.get_current_function_name())
    def register_authorize(self, token_key):
        db_base_not_implement(db_util.get_current_function_name())
        
    ''' manage '''
    def manage_metadata(self, body, token_key, callback):
        db_base_not_implement(db_util.get_current_function_name())
    def manage_setting(self, body, token_key, callback):
        db_base_not_implement(db_util.get_current_function_name())
    def manage_bill(self, body, token_key, callback):
        db_base_not_implement(db_util.get_current_function_name())
    def manage_feedback(self, body, token_key, callback):
        db_base_not_implement(db_util.get_current_function_name())
    def manage_inquiry(self, body, token_key, callback):
        db_base_not_implement(db_util.get_current_function_name())
        
    ''' access'''
    def access_type_1(self, token_key, query, validation, capability):
        db_base_not_implement(db_util.get_current_function_name())
    def access_type_2(self, token_key, access_token_key, validation, query, data):
        db_base_not_implement(db_util.get_current_function_name())
    def access_type_3(self, access_token_key, access_result):
        db_base_not_implement(db_util.get_current_function_name())
    '''def access(self, access_token_key, timestamp, manage_token_key, callback, method, target):
        db_base_not_implement(db_util.get_current_function_name())    '''
        
class MyTestParser(HttpRequestParserBase):
    def __init__(self):
        pass
    
    def register_resource_init(self, name, url, desc, callback, method, target):
        print "hello myparser cool"