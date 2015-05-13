import scrapy
from datetime import datetime
from scrapers.items import *
from scrapers.music_apis import MusicHelper


class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    base_url = 'http://www.metacritic.com'
    allowed_domains = ['metacritic.com']
    start_urls = [
        'http://www.metacritic.com/browse/albums/release-date/new-releases/date?view=detailed',
    ]
    download_delay = 3
    apis = MusicHelper()

    def parse(self, response):
        album_links = response.css('li.product').xpath('.//h3/a/@href').extract()
        for link in album_links[-5:]:
            absoluteURL = self.base_url + link
            request = scrapy.Request(absoluteURL, callback=self.parse_album_page)
            yield request

    def parse_album_page(self, response):
        meta_info = response.css('div.content_head.product_content_head.album_content_head')
        release_date_sel = meta_info.css('li.summary_detail.release span.data::text')
        release_date = self.safe_extract(release_date_sel)
        release_date = datetime.strptime(release_date, '%b %d, %Y').date()

        # External APIs have no info on upcoming releases, so we ignore them
        if datetime.now().date() < release_date:
            return 

        album = AlbumItem()
        artist = ArtistItem()

        album_name_sel = meta_info.css('span a.hover_none span::text')
        album_name = self.safe_extract(album_name_sel)
        artist_name_sel = meta_info.css('a span.band_name::text')
        artist_name = self.safe_extract(artist_name_sel)

        mb_album = self.apis.mb_find_album(album_name, artist=artist_name)
        if not mb_album:
            return

        artist_credit = mb_album['artist-credit'][0]['artist']['name']
        artist_id = mb_album['artist-credit'][0]['artist']['id']
        if artist_name.lower() != artist_credit.lower():
            return

        lf_artist = self.apis.lastfm.get_artist_by_mbid(artist_id)
        artist['mbid'] = artist_id
        artist['name'] = artist_name
        artist['bio'] = MusicHelper.lastfm_clean_summary(lf_artist.get_bio_summary())
        artist['bio_url'] = lf_artist.get_url()
        artist['tags'] = [tag.item.get_name().lower() for tag in lf_artist.get_top_tags(limit=6)]
        artist['familiarity'] = self.apis.en_get_artist_familiarity(artist_id)
        artist['trending'] = self.apis.en_get_artist_trending(artist_id)

        mb_release = self.apis.mb_get_album_by_id(mb_album['id'])
        album_date = mb_release['release-group']['first-release-date']
        album['date'] = datetime.strptime(album_date, '%Y-%m-%d')
        album['artist'] = artist
        album['mbid'] = mb_album['id']
        album['name'] = mb_album['title']

        album_score_sel = response.css('.metascore_w span::text')
        album_score = self.safe_extract(album_score_sel, default='0')
        album['score'] = album_score
        album['score_url'] = response.url

        album_summary_sel = response.css('.summary_detail.product_summary span.data span::text')
        album_summary = self.safe_extract(album_summary_sel)
        album['summary'] = album_summary

        yield album

    def safe_extract(self, selector, default=''):
        return selector[0].extract().strip() if selector else default


