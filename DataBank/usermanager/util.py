'''
Created on Dec 30, 2011

@author: jianhuashao
'''

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME

USERNAME = "username"
PASSWROD = "password"
NEXT = "next"

login_path = "/accounts/login/"
def check_user_login(request):
    user = request.user
    print user.is_authenticated()
    if not user.is_authenticated():
        # all need to pass in the redirect
        url = login_path+"?"+REDIRECT_FIELD_NAME+"="+request.path+""
        #url = login_in_path
        print url
        return HttpResponseRedirect(url) 
        #return HttpResponseRedirect("/accounts/login/")
    else:
        return None
    
def check_user(request):
    user = request.user
    context_user = {
        "is_authenticated":user.is_authenticated(),
        "name": user.username,
            }
    return context_user