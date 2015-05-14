from django.conf.urls import patterns, include, url
from django.contrib import admin
from base.views import *

urlpatterns = patterns('',
    url(r'^artists/$', ArtistList.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
)
