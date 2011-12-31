'''
Created on Dec 30, 2011

@author: jianhuashao
'''
from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^hello/$',     hello), 
    url(r'^test/',     test_http_protocol),  
    url(r'^',     sauth_views_main),   
)