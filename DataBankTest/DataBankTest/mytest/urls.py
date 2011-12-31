'''
Created on Dec 16, 2011

@author: jianhuashao
'''
from views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^test_action/',    test_action),
)