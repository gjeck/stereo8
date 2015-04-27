import scrapy, datetime
from scrapers.items import *

class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    allowed_domains = ['metacritic.com']
    start_urls = [
        'http://www.metacritic.com/browse/albums/release-date/new-releases/date?view=detailed',
    ]

    def parse(self, response):
        elems = response.css('li.product')
        for el in elems:
            a = ArtistItem()
            a['name'] = el.xpath('.//h3/a/text()').extract()
            a['bio'] = ''
            yield a
