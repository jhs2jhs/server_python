'''
Created on Dec 12, 2011

@author: jianhuashao
'''

from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render_to_response
import http_protocol_parser.request_parse as db_parser

def test_action(request):
    db_parser.parse_http_request_to_dict(request)
    return HttpResponse("hello:")

def user_home(request):
    context = {
        "user": "hello"
            }
    return render_to_response("user_home.html", context)