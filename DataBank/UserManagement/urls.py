from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^login/',    user_login),
    url(r'^register/', user_register),
    url(r'^logout/',   user_logout), 
    
    url(r'^temptest/', template_test),
    url(r'^usertest/', user_test),
)

