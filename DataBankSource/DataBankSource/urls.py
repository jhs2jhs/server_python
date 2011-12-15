from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DataBankSource.views.home', name='home'),
    # url(r'^DataBankSource/', include('DataBankSource.foo.urls')),
    url(r'^hello/', hello),
    url(r'^user/', user_home),
    url(r'^accounts/', include('UserManagement.urls')),
    url(r'^sauth/', include('SimpleAuth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
