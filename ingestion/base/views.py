from django.shortcuts import render
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework_api_key.permissions import HasAPIKey
from taggit.models import Tag
from .models import (
    Album,
    Artist,
    BaseModel,
    Image,
    Publisher,
    Review,
    Track,
)
from .serializers import (
    AlbumSerializer,
    BaseIndexSerializer,
    ArtistSerializer,
    ImageSerializer,
    PublisherSerializer,
    ReviewSerializer,
    TrackSerializer,
)


def get_permissions():
    if settings.DEBUG:
        return [AllowAny]
    else:
        return [HasAPIKey | IsAuthenticated]

class AlbumList(generics.ListCreateAPIView):
    permission_classes = get_permissions()
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ArtistList(generics.ListCreateAPIView):
    permission_classes = get_permissions()
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ImageList(generics.ListCreateAPIView):
    permission_classes = get_permissions()
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class PublisherList(generics.ListCreateAPIView):
    permission_classes = get_permissions()
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class ReviewList(generics.ListCreateAPIView):
    permission_classes = get_permissions()
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class TrackList(generics.ListCreateAPIView):
    permission_classes = get_permissions()
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

