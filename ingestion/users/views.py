from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken import views as auth_views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import User

