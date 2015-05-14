import datetime
from haystack import indexes
from base.models import *


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateField(model_attr='date')

    def get_model(self):
        return Album

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date__lte=datetime.datetime.now())
