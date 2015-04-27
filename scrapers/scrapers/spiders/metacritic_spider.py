import scrapy, datetime
from scrapers.items import *

class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    base_url = 'http://www.metacritic.com'
    allowed_domains = ['metacritic.com']
    start_urls = [
        'http://www.metacritic.com/browse/albums/release-date/new-releases/date?view=detailed',
    ]

    def parse(self, response):
        album_links = response.css('li.product').xpath('.//h3/a/@href').extract()
        for link in album_links:
            absoluteURL = self.base_url + link
            request = scrapy.Request(absoluteURL, callback=self.parse_album_page)
            yield request

    def parse_album_page(self, response):
        artist = ArtistItem()
        album = AlbumItem()
        label = LabelItem()

        meta_info = response.css('.product_title')
        album_title = meta_info.css('span a.hover_none span::text')[0].extract().strip()
        artist_name = meta_info.css('span.band_name::text')[0].extract().strip()
        album_score_sel = response.css('.metascore_w span::text')
        album_score = album_score_sel[0].extract().strip() if len(album_score_sel) else '0'
        album_summary = response.css('.summary_detail.product_summary span.data span::text')[0].extract()
        print artist_name, album_title, album_score

