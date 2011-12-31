'''
Created on Dec 12, 2011

@author: jianhuashao
'''

import sauth.util as sutil
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render_to_response


def hello(request):
    return HttpResponse("hello:")

def user_home(request):
    context = {
        "user": sutil.check_user(request),
            }
    return render_to_response("user_home.html", context)