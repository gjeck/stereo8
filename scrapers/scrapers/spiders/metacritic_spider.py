import scrapy, datetime
from scrapers.items import *
from scrapers.music_apis import MusicHelper


class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    base_url = 'http://www.metacritic.com'
    allowed_domains = ['metacritic.com']
    start_urls = [
        'http://www.metacritic.com/browse/albums/release-date/new-releases/date?view=detailed',
    ]
    download_delay = 2
    apis = MusicHelper()

    def parse(self, response):
        album_links = response.css('li.product').xpath('.//h3/a/@href').extract()
        for link in album_links[-2:]:
            absoluteURL = self.base_url + link
            request = scrapy.Request(absoluteURL, callback=self.parse_album_page)
            yield request

    def parse_album_page(self, response):
        album = AlbumItem()
        artist = ArtistItem()

        meta_info = response.css('div.content_head.product_content_head.album_content_head')

        album_name_sel = meta_info.css('span a.hover_none span::text')
        album_name = self.safe_extract(album_name_sel)
        album['name'] = album_name

        artist_name_sel = meta_info.css('a span.band_name::text')
        artist_name = self.safe_extract(artist_name_sel)
        artist['name'] = artist_name

        release_date_sel = meta_info.css('li.summary_detail.release span.data::text')
        release_date = self.safe_extract(release_date_sel)
        album_date = datetime.datetime.strptime(release_date, '%b %d, %Y').date()
        album['date'] = album_date

        album_score_sel = response.css('.metascore_w span::text')
        album_score = self.safe_extract(album_score_sel, default='0')
        album['score'] = album_score
        album['score_url'] = response.url

        album_summary_sel = response.css('.summary_detail.product_summary span.data span::text')
        album_summary = self.safe_extract(album_summary_sel)
        album['summary'] = album_summary

        mb_album = self.apis.mb_find_album(album_name, artist_name)
        album['mbid'] = mb_album['id']
        artist['mbid'] = mb_album['artist-credit'][0]['artist']['id']
        artist['bio'] = ''
        album['artist'] = artist

        yield album

    def safe_extract(self, selector, default=''):
        return selector[0].extract().strip() if len(selector) else default


