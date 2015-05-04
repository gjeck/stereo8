from scrapy.exceptions import DropItem
from scrapers.items import *
from base.models import *

class DjangoItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AlbumItem):
            self.process_album(item, spider)

        return item

    def process_album(self, item, spider):
        album, created = Album.objects.update_or_create(mbid=item['mbid'], defaults={
	    'date': item['date'],
	    'name': item['name'],
            'summary': item['summary'],
            'score': item['score'],
            'score_url': item['score_url'],
	})
	if created:
	    print 'created'
	else:
	    print 'updated'
	return item
        




