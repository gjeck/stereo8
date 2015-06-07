from django.shortcuts import render
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from rest_framework import generics
from .models import (
    Album,
    Artist,
    Image,
    Publisher,
    Review,
    Track,
)
from .serializers import (
    AlbumSerializer,
    AlbumIndexSerializer,
    ArtistSerializer,
    ImageSerializer,
    PublisherSerializer,
    ReviewSerializer,
    TrackSerializer,
)


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumSearchQuerySet(SearchQuerySet):
    model = Album

class EmptyAlbumSearchQuerySet(EmptySearchQuerySet):
    model = Album

class AlbumSearchViewSet(generics.ListAPIView):
    serializer_class = AlbumIndexSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptyAlbumSearchQuerySet()

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            queryset = AlbumSearchQuerySet() \
                            .filter(content=query) \
                            .load_all()

        return queryset


class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


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

