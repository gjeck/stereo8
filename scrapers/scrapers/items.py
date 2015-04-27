# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem

class AlbumItem(DjangoItem):
    django_model = Album
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
