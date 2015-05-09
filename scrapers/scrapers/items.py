import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from base.models import *

class AlbumItem(DjangoItem):
    django_model = Album
    artist = scrapy.Field()
    pass

class ArtistItem(DjangoItem):
    django_model = Artist
    pass

class LabelItem(DjangoItem):
    django_model = Label
    pass

class PublisherItem(DjangoItem):
    django_model = Publisher
    pass

class ReviewItem(DjangoItem):
    django_model = Review
    pass

class Track(DjangoItem):
    django_model = Track
    pass
