import scrapy, datetime, musicbrainzngs
from scrapers.items import *


class MusicBrainzHelper():

    def __init__(self):
        musicbrainzngs.set_useragent('Stereo8', '0.1.0', 'https://github.com/gjeck/stereo8')

    def get_album(self, name, artist):
        response = musicbrainzngs.search_release_groups(query=name, artist=artist, limit=1)
        release_list = response['release-group-list']
        return release_list[0]

class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    base_url = 'http://www.metacritic.com'
    allowed_domains = ['metacritic.com']
    start_urls = [
        'http://www.metacritic.com/browse/albums/release-date/new-releases/date?view=detailed',
    ]
    download_delay = 2
    mb = MusicBrainzHelper()

    def parse(self, response):
        album_links = response.css('li.product').xpath('.//h3/a/@href').extract()
        for link in album_links[-2:]:
            absoluteURL = self.base_url + link
            request = scrapy.Request(absoluteURL, callback=self.parse_album_page)
            yield request

    def parse_album_page(self, response):
        artist = ArtistItem()
        album = AlbumItem()
        label = LabelItem()

        meta_info = response.css('div.content_head.product_content_head.album_content_head')
        album_name = meta_info.css('span a.hover_none span::text')[0].extract().strip()
        artist_name = meta_info.css('a span.band_name::text')[0].extract().strip()
        release_date = meta_info.css('li.summary_detail.release span.data::text')[0].extract().strip()
        album_date = datetime.datetime.strptime(release_date, '%b %d, %Y').date()

        album_score_sel = response.css('.metascore_w span::text')
        album_score = album_score_sel[0].extract().strip() if len(album_score_sel) else '0'

        album_summary_sel = response.css('.summary_detail.product_summary span.data span::text')
        album_summary = album_summary_sel[0].extract() if len(album_summary_sel) else ''

        mb_album = self.mb.get_album(album_name, artist_name)

        album['mbid'] = mb_album['id']
        album['date'] = album_date
        album['name'] = album_name
        album['summary'] = album_summary
        album['score'] = album_score
        album['score_url'] = response.url

        yield album


