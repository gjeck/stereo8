from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^artists/$', views.ArtistList.as_view()),
)

