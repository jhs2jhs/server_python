"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import http_protocol_parser.test_db as db_test
import db_util.util as db_util

from django.test import TestCase
from django.test.client import Client



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        print "hello mytest"
        
    def test_action(self):
        db_test.test_print_begin(db_util.get_current_function_name()) 
        c = Client()
        response = c.post('/test_action', {"action":"access"})
        print response
        db_test.test_print_end("NotDjangoHttpRequestError can be captured in Error type")

