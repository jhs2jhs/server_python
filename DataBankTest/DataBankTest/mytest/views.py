# Create your views here.
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render_to_response
import http_protocol_parser.parser_class_base as my_parser
import http_protocol_parser.request_parse as db_parser

def test_action(request):
    db_parser.parse_http_request_to_dict(my_parser.MyTestParser, request)
    print "..finish"
    db_parser.example_http_encode()
    return HttpResponse("hello:")
