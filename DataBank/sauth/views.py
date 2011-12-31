from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
# Create your views here.

import http_protocol_parser.parser_class_base as parser_base
import http_protocol_parser.request_parse as db_parser
import db_util.util as db_util

def hello(request):
    db_parser.example_http_encode()
    return HttpResponse(" sauth hello")

def test_http_protocol(request):
    db_parser.parse_http_request_to_dict(parser_base.MyTestParser, request)
    return HttpResponse("hello:")


class SAUTHParser(parser_base.HttpRequestParserBase):
    '''parse the http request of DataBank'''
    def __init__(self):
        pass
    
    ''' register '''
    def register_token_init(self, token_key):
        parser_base.db_base_not_implement(db_util.get_current_function_name())  
    def register_resource_init(self, name, url, desc, callback, method, target):
        print "hello resource"
    def register_request(self, token_key, callback, method, target):
        parser_base.db_base_not_implement(db_util.get_current_function_name())
    def register_authorize(self, token_key):
        parser_base.db_base_not_implement(db_util.get_current_function_name())
         
         
def sauth_views_main(request):
    db_parser.parse_http_request_to_dict(SAUTHParser, request)
    return HttpResponse("hello:")