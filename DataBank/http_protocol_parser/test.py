'''
Created on Dec 16, 2011

@author: jianhuashao
'''
import random
import unittest
import inspect
import sys
import exception_db as db_except
import http_request_parse_db as db_http
import util_db as db_util

from django.http import QueryDict
from django.test.client import Client
#from django.utils import unittest

def test_print_begin(msg):
    print "************************"
    print "** test: "+str(msg)+" **"
    
def test_print_end(msg):
    print "** result: "+str(msg)+" **"
    print "************************"

class TestLibs(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)

    def test_djangohttprequestchecking(self):
        test_print_begin(db_util.get_current_function_name()) 
        try:
            db_http.parse_http_request_to_dict("hello")
        except db_except.Error as e:
            self.assertTrue("hello", e.org)
            test_print_end("NotDjangoHttpRequestError can be captured in Error type")
            
    def test_gethttpparams(self):
        test_print_begin(db_util.get_current_function_name()) 
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'smith'})
        print response
        test_print_end("NotDjangoHttpRequestError can be captured in Error type")

    
if __name__ == '__main__':
    unittest.main()
    