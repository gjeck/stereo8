from django.conf.urls import include, url
from rest_framework.authtoken import views as auth_views
from . import views as user_views

app_name = 'users'

urlpatterns = [
    url(r'^token/', auth_views.obtain_auth_token),
]
