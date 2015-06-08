import datetime
from haystack import indexes
from taggit.models import Tag
from .models import (
    Album,
    Artist,
)


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Album

    def index_queryset(self, using=None):
        return self.get_model() \
                   .objects \


class ArtistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        return self.get_model() \
                   .objects \


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='slug')
    
    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        return self.get_model() \
                   .objects
