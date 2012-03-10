'''
Created on Dec 12, 2011

@author: jianhuashao
'''

import usermanager.util as uutil
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render_to_response


def hello(request):
    return HttpResponse("hello: hello")

def user_home(request):
    context = {
        "user": uutil.check_user(request),
            }
    return render_to_response("user_home.html", context)


def world(request):
    context = {
        "hello": "mememem",
               }
    return render_to_response("NewFile.html", context)