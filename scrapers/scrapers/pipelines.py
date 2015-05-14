import django
from scrapy.exceptions import DropItem
from scrapers.items import *
from base.models import *

class DjangoItemPipeline(object):
    django.setup()

    def process_item(self, item, spider):
        if isinstance(item, AlbumItem):
            self.process_album(item, spider)

        return item

    def process_album(self, item, spider):
        artist_image, created = Image.objects.update_or_create(mbid=item['artist']['mbid'], defaults={
            'large': item['artist']['image']['large'],
            'medium': item['artist']['image']['medium'],
            'small': item['artist']['image']['small'],
        })

        artist, created = Artist.objects.update_or_create(mbid=item['artist']['mbid'], defaults={
            'bio': item['artist']['bio'],
            'bio_url': item['artist']['bio_url'],
            'familiarity': item['artist']['familiarity'],
            'image': artist_image,
            'name': item['artist']['name'],
            'trending': item['artist']['trending'],
        })
        artist.tags.add(*item['artist']['tags'])

        album_image, created = Image.objects.update_or_create(mbid=item['mbid'], defaults={
            'large': item['image']['large'],
            'medium': item['image']['medium'],
            'small': item['image']['small'],
        })

        album, created = Album.objects.update_or_create(mbid=item['mbid'], defaults={
            'artist': artist,
            'date': item['date'],
            'image': album_image,
            'name': item['name'],
            'summary': item['summary'],
            'score': item['score'],
            'score_url': item['score_url'],
        })
        album.tags.add(*item['tags'])
        return item





