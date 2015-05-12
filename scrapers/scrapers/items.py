import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from base.models import *

class AlbumItem(DjangoItem):
    django_model = Album
    artist = scrapy.Field()

class ArtistItem(DjangoItem):
    django_model = Artist
    tags = scrapy.Field()

class PublisherItem(DjangoItem):
    django_model = Publisher

class ReviewItem(DjangoItem):
    django_model = Review

class Track(DjangoItem):
    django_model = Track

