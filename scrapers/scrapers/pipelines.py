from scrapy.exceptions import DropItem
from scrapers.items import *
from base.models import *

class DjangoItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AlbumItem):
            self.process_album(item, spider)

        return item

    def process_album(self, item, spider):
        artist, created = Artist.objects.update_or_create(mbid=item['artist']['mbid'], defaults={
            'name': item['artist']['name'],
            'bio': item['artist']['bio'],
        })

        album, created = Album.objects.update_or_create(mbid=item['mbid'], defaults={
            'artist': artist,
	    'date': item['date'],
	    'name': item['name'],
            'summary': item['summary'],
            'score': item['score'],
            'score_url': item['score_url'],
	})
	return item
        




