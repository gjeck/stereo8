from django.shortcuts import render
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from rest_framework import generics
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


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class BaseSearchQuerySet(SearchQuerySet):
    model = BaseModel


class EmptyBaseSearchQuerySet(EmptySearchQuerySet):
    model = BaseModel


class SearchViewSet(generics.ListAPIView):

    def get_serializer_class(self, *args, **kwargs):
        return BaseIndexSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptyBaseSearchQuerySet()
        query = request.GET.get('q')

        if query is not None:
            models = self.get_models(request)
            queryset = self.filtered_query_set(query, models)
        
        return queryset

    def get_models(self, request):
        allowed_models = {
            'artist': Artist,
            'album': Album,
            'tag': Tag,
        }
        param = request.GET.get('models')
        if param:
            model_names = param.split(',')
            model_list = [
                allowed_models.get(model.lower()) for model in model_names
            ]
            return list(filter(None, model_list))
        else:
            return list(allowed_models.values())

    def filtered_query_set(self, query, models):
        return BaseSearchQuerySet() \
                    .models(*models) \
                    .filter(content=query) \


class AutoSearchViewSet(SearchViewSet):

    def filtered_query_set(self, query, models):
        return BaseSearchQuerySet() \
                    .models(*models) \
                    .autocomplete(content_auto=query) \


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

