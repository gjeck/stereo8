import datetime
from haystack import indexes
from .models import (
    Album,
    Artist,
)


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Album

    def index_queryset(self, using=None):
        return self.get_model() \
                   .objects \

class ArtistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        return self.get_model() \
                   .objects \

