'''
Created on Dec 12, 2011

@author: jianhuashao
'''

import DBUtil.sutil as myutil
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render_to_response


def hello(request):
    return HttpResponse("hello:"+myutil.hello)

def user_home(request):
    context = {
        "user": myutil.check_user(request),
            }
    return render_to_response("user_home.html", context)