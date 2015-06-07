from django.shortcuts import render
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from rest_framework import generics
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


class BaseSearchQuerySet(SearchQuerySet):
    model = BaseModel

class EmptyBaseSearchQuerySet(EmptySearchQuerySet):
    model = BaseModel

class SearchViewSet(generics.ListAPIView):

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptyBaseSearchQuerySet()

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            queryset = BaseSearchQuerySet() \
                            .filter(content=query) \
                            .load_all()

        return queryset

    def get_serializer_class(self, *args, **kwargs):
        return AlbumIndexSerializer


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

