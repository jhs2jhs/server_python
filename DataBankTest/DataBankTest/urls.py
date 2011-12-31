from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DataBankTest.views.home', name='home'),
    url(r'^', include('DataBankTest.mytest.urls')),
    #url(r'^test_action/', test_action),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
