'''
Created on Dec 12, 2011

@author: jianhuashao
'''
import uuid
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME

hello = "hello"

def check_user(request):
    user = request.user
    context_user = {
        "is_authenticated":user.is_authenticated(),
        "name": user.username,
            }
    return context_user

login_in_path = "/accounts/login/"
def check_user_login(request):
    user = request.user
    print user.is_authenticated()
    if not user.is_authenticated():
        # all need to pass in the redirect
        url = login_in_path+"?"+REDIRECT_FIELD_NAME+"="+request.path+""
        #url = login_in_path
        print url
        return HttpResponseRedirect(url)
        #return HttpResponseRedirect("/accounts/login/")
    else:
        return None


def get_http_param(request, key):
    if (request.POST.get(key) != None): 
        return request.POST.get(key)
    elif (request.GET.get(key) != None):
        return request.GET.get(key)
    else:
        return None
    
def new_key():
    return uuid.uuid4().hex

def new_secret():
    return uuid.uuid4().hex

def new_token():
    return uuid.uuid4().hex


    
    