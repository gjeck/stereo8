from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import generics
from .models import (
    Artist,
    Album,
    Image,
    Publisher,
    Review,
    Track,
)
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    ImageSerializer,
    PublisherSerializer,
    ReviewSerializer,
    TrackSerializer,
)


class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class PublisherList(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

