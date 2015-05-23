from django.conf.urls import patterns, include, url
from django.contrib import admin
from base.views import ArtistList


urlpatterns = patterns('',
    url(r'^artists/$', ArtistList.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('haystack.urls')),
)
