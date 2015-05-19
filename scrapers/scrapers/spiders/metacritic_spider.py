import scrapy
from datetime import datetime
from scrapers.items import *
from scrapers.music_apis import MusicHelper
from urlparse import urlparse


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
            absolute_url = self.base_url + link
            request = scrapy.Request(absolute_url, callback=self.parse_album_page)
            yield request

    def parse_album_page(self, response):
        meta_info = response.css('div.content_head.product_content_head.album_content_head')
        release_date_sel = meta_info.css('li.summary_detail.release span.data::text')
        release_date = self.safe_extract(release_date_sel)
        release_date = datetime.strptime(release_date, '%b %d, %Y').date()

        # External APIs have no info on upcoming releases, so we ignore them
        if datetime.now().date() < release_date:
            return 

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
        artist_image = ImageItem()
        artist_image['large'] = lf_artist.get_cover_image(4)
        artist_image['medium'] = lf_artist.get_cover_image(3)
        artist_image['small'] = lf_artist.get_cover_image(2)

        lf_album = self.apis.lastfm.get_album(artist_name, mb_album['title'])
        album_image = ImageItem()
        album_image['large'] = lf_album.get_cover_image(4)
        album_image['medium'] = lf_album.get_cover_image(3)
        album_image['small'] = lf_album.get_cover_image(2)

        sp_album = self.apis.sp_find_album(mb_album['title'], artist=artist_name)
        artist = ArtistItem()
        artist['mbid'] = artist_id
        artist['name'] = artist_name
        artist['bio'] = MusicHelper.lastfm_clean_summary(lf_artist.get_bio_summary())
        artist['bio_url'] = lf_artist.get_url()
        artist['tags'] = [MusicHelper.lastfm_clean_tag(tag) for tag in lf_artist.get_top_tags(limit=6)]
        artist['familiarity'] = self.apis.en_get_artist_familiarity(artist_id)
        artist['trending'] = self.apis.en_get_artist_trending(artist_id)
        artist['spotify_id'] = sp_album.get('artists', [{}])[0].get('id', '')
        artist['spotify_url'] = sp_album.get('artists', [{}])[0].get('external_urls', {}).get('spotify', '')
        artist['image'] = artist_image

        mb_release = self.apis.mb_get_album_by_id(mb_album['id'])
        album_date_string = mb_release['release-group']['first-release-date']
        album_date = datetime.strptime(album_date_string, '%Y-%m-%d')
        album = AlbumItem()
        album['date'] = album_date
        album['artist'] = artist
        album['mbid'] = mb_album['id']
        album['name'] = mb_album['title']
        album['popularity'] = sp_album.get('popularity', 0.0) / 100.0
        album['spotify_id'] = sp_album.get('id', '')
        album['spotify_url'] = sp_album.get('external_urls', {}).get('spotify', '')
        album['image'] = album_image

        album_score_sel = response.css('.metascore_w span::text')
        album_score = self.safe_extract(album_score_sel, default='0')
        album['score'] = album_score
        album['score_url'] = response.url

        album_summary_sel = response.css('.summary_detail.product_summary span.data span::text')
        album_summary = self.safe_extract(album_summary_sel)
        album['summary'] = album_summary

        album_tags_sel = response.css('li.summary_detail.product_genre span.data::text').extract()
        album['tags'] = [MusicHelper.clean_tag(tag) for tag in album_tags_sel]

        see_all_reviews = self.safe_extract(response.css('.reviews_module .see_all a::attr(href)'), default=None)
        if see_all_reviews:
            absolute_url = self.base_url + see_all_reviews
            request = scrapy.Request(absolute_url, callback=self.parse_all_reviews_page)
            request.meta['album'] = album
            yield request
        else:
            album['reviews'] = self.parse_reviews_from_response(response)
            yield album

    def parse_all_reviews_page(self, response):
        album = response.meta['album']
        album['reviews'] = self.parse_reviews_from_response(response)
        yield album

    def safe_extract(self, selector, default=''):
        return selector[0].extract().strip() if selector else default

    def parse_base_url(self, full_url):
        parsed_url = urlparse(full_url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    def parse_reviews_from_response(self, response):
        reviews = response.css('li.review.critic_review')
        review_list = []
        for r in reviews:
            rev_url = self.safe_extract(r.css('a.external::attr(href)'))
            rev_date = self.safe_extract(r.css('.date::text'))

            publisher = PublisherItem()
            publisher['name'] = self.safe_extract(r.css('.source a::text'))
            publisher['url'] = self.parse_base_url(rev_url)

            review = ReviewItem()
            review['url'] = rev_url
            review['publisher'] = publisher
            review['score'] = self.safe_extract(r.css('.review_grade div::text'), default='0')
            review['summary'] = self.safe_extract(r.css('.review_body::text')).replace('\n', '').strip()
            review['date'] = datetime.strptime(rev_date, '%b %d, %Y').date()
            review_list.append(review)
        return review_list



