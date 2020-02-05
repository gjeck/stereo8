import scrapy
from scrapy_djangoitem import DjangoItem
from base.models import (
    Album,
    Artist,
    Image,
    Publisher,
    Review,
    Track,
    SonicInfo,
)


class AlbumItem(DjangoItem):
    django_model = Album
    artist = scrapy.Field()
    image = scrapy.Field()
    tags = scrapy.Field()
    reviews = scrapy.Field()
    tracks = scrapy.Field()


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


class TrackItem(DjangoItem):
    django_model = Track
    sonic_info = scrapy.Field()

class SonicInfoItem(DjangoItem):
    django_model = SonicInfo
    acousticness = scrapy.Field(default=0.0)
    daceability = scrapy.Field(default=0.0)
    energy = scrapy.Field(default=0.0)
    instrumentalness = scrapy.Field(default=0.0)
    liveness = scrapy.Field(default=0.0)
    loudness = scrapy.Field(default=0.0)
    speechiness = scrapy.Field(default=0.0)
    tempo = scrapy.Field(default=0.0)
    valence = scrapy.Field(default=0.0)
    mode = scrapy.Field()


