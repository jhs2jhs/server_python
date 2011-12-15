from django.conf.urls.defaults import *

import views_service as service
import views_consumer as consumer

urlpatterns = patterns('',
    url(r'^request_token/$',    service.request_token,      name='oauth_request_token'),
    url(r'^authorize/$',        service.user_authorization, name='oauth_user_authorization'),
    url(r'^access_token/$',     service.access_token,       name='oauth_access_token'),
    
    url(r'^resource/add/', service.resource_add), 
    url(r'^consumer/add/', service.consumer_add), 
    
    url(r'^generate_request_token/$',     service.generate_request_token),
    url(r'^service_request/$',     service.service_request),
    url(r'^generate_access_token/$',     service.generate_access_token),
    
    
    url(r'^consumer_request/$',     consumer.consumer_request), 
)

