import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from base.models import *

class AlbumItem(DjangoItem):
    django_model = Album
    artist = scrapy.Field()
    image = scrapy.Field()
    tags = scrapy.Field()
    reviews = scrapy.Field()

class ArtistItem(DjangoItem):
    django_model = Artist
    image = scrapy.Field()
    tags = scrapy.Field()

class ImageItem(DjangoItem):
    django_model = Image

class PublisherItem(DjangoItem):
    django_model = Publisher

class ReviewItem(DjangoItem):
    django_model = Review
    publisher = scrapy.Field()

class Track(DjangoItem):
    django_model = Track

