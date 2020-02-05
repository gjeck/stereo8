import scrapy
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from dateutil import parser as dateparser
from fuzzywuzzy import fuzz
from scrapers.items import (
    AlbumItem,
    ArtistItem,
    ImageItem,
    TrackItem,
    ReviewItem,
    PublisherItem,
    SonicInfoItem,
)
from scrapers.music_apis import MusicHelper
from urllib.parse import urlparse

class MetacriticSingleSpider(Spider):
    name = 'meta-album'
    allowed_domains = ['metacritic.com']
    download_delay = 10
    metacritic_spider = {}

    def __init__(self, url=None, *args, **kwargs):
        super(MetacriticSingleSpider, self).__init__(*args, **kwargs)
        self.metacritic_spider = MetacriticSpider(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = []

    def parse(self, response):
        return self.metacritic_spider.parse_album_page(response)

class MetacriticSpider(CrawlSpider):
    name = 'metacritic'
    allowed_domains = ['metacritic.com']
    download_delay = 10
    apis = MusicHelper.build()

    def __init__(self, crawl_all=None, *args, **kwargs):
        super(MetacriticSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://www.metacritic.com'
        if crawl_all:
            self.start_urls = [
                '{0}/browse/albums/artist'.format(self.base_url),
            ]
            self.rules = (
                Rule(LinkExtractor(allow=r'\/albums\/artist\/[A-z]',unique=True )),
                Rule(
                    LinkExtractor(allow=r'\/music\/.*\/.*',unique=True ),
                    callback='parse_album_page'
                ),
            )
        else:
            to_start = 'browse/albums/release-date/new-releases/date?view=detailed'
            self.start_urls = [
                '{0}/{1}'.format(self.base_url, to_start),
            ]
            self.rules = (
                Rule(
                    LinkExtractor(allow=r'\/music\/.*\/.*',unique=True ),
                    callback='parse_album_page', follow=True
                ),
            )
        super(MetacriticSpider, self)._compile_rules()

    def parse_album_page(self, response):
        meta_info = response.css(
            'div.content_head.product_content_head.album_content_head'
        )
        release_date_sel = meta_info.css(
            'li.summary_detail.release span.data::text'
        )
        release_date = self.safe_extract(release_date_sel)
        if not release_date:
            self.logger.info('METACRITIC: Release date is empty'.format(album_name))
            return 

        release_date = dateparser.parse(release_date).date()

        album_name_sel = meta_info.css('div.product_title h1::text')
        album_name = self.safe_extract(album_name_sel)
        artist_name_sel = meta_info.css('a span.band_name::text')
        artist_name = self.safe_extract(artist_name_sel)

        # External APIs have no info on upcoming releases, so we ignore them
        if datetime.now().date() < release_date:
            self.logger.info('METACRITIC: Album {0} has not been released yet'.format(album_name))
            return

        self.logger.info('METACRITIC: extracted from page (release_date: {0}, artist: {1}, album: {2})'.format(release_date, artist_name, album_name))

        mb_album = self.apis.mb_find_album(album_name, artist=artist_name)
        if not mb_album:
            self.logger.info('METACRITIC: Album {0} not found on musicbrainz'.format(album_name))
            return

        artist_credit = mb_album['artist-credit'][0]['artist']['name']
        artist_id = mb_album['artist-credit'][0]['artist']['id']
        artist_confidence = fuzz.token_sort_ratio(
            artist_name.lower(),
            artist_credit.lower()
        )

        # Do some fuzzy matching on artist, return if not confident
        if artist_confidence < 55:
            self.logger.info('METACRITIC: Fuzzy matching {0} and {1} confidence too low to continue'.format(artist_name, artist_credit))
            return

        self.logger.info('METACRITIC: got musicbrainz artist: {0}, id: {1}, album_title: {2}'.format(artist_credit, artist_id, mb_album['title'])) 

        sp_album = self.apis.sp_find_album(
            mb_album['title'], artist=artist_name
        )

        if not sp_album:
            self.logger.info('METACRITIC: album not found on spotify')
            return

        sp_artist = self.apis.sp_find_artist(artist_name)

        if not sp_artist:
            self.logger.info('METACRITIC: artist not found on spotify')
            return

        lf_artist = None
        try:
            lf_artist = self.apis.lastfm.get_artist_by_mbid(artist_id)
        except:
            self.logger.info('METACRITIC: artist_id {0} not found on last.fm doing search instead'.format(artist_id))

        try:
            lf_artist_search = self.apis.lastfm.search_for_artist(artist_credit)
            lf_artist_search_results = lf_artist_search.get_next_page()
            for result_artist in lf_artist_search_results:
                compare_confidence = fuzz.token_sort_ratio(artist_name, result_artist.name)
                if compare_confidence > 50:
                    lf_artist = result_artist
                    break
        except:
            self.logger.info('METACRITIC: artist {0} not found on last.fm. Ending'.format(artist_credit))
            return

        if not lf_artist:
            self.logger.info('METACRITIC: artist {0} not found on last.fm. Ending'.format(artist_credit))
            return

        artist_image = ImageItem()
        artist_image['large'] = lf_artist.get_cover_image(4)
        artist_image['medium'] = lf_artist.get_cover_image(3)
        artist_image['small'] = lf_artist.get_cover_image(2)

        lf_album = self.apis.lastfm.get_album(artist_name, mb_album['title'])
        album_image = ImageItem()
        album_image['large'] = lf_album.get_cover_image(4)
        album_image['medium'] = lf_album.get_cover_image(3)
        album_image['small'] = lf_album.get_cover_image(2)

        artist = ArtistItem()
        artist['mbid'] = artist_id
        artist['name'] = artist_name
        artist['bio'] = MusicHelper.lastfm_clean_summary(
            lf_artist.get_bio_summary()
        )
        artist['bio_url'] = lf_artist.get_url()
        artist['tags'] = [genre.lower() for genre in sp_artist.get('genres', [])]
        if not artist['tags']:
            artist['tags'] = [
                MusicHelper.lastfm_clean_tag(tag) for tag
                in lf_artist.get_top_tags(limit=6)
            ]
        artist['spotify_id'] = sp_album.get('artists', [{}])[0] \
                                       .get('id', '')
        artist['spotify_url'] = sp_album.get('artists', [{}])[0] \
                                        .get('external_urls', {}) \
                                        .get('spotify', '')
        artist['image'] = artist_image

        mb_release = self.apis.mb_get_album_by_id(mb_album['id'])
        album_date_string = mb_release['release-group']['first-release-date']
        album_date = dateparser.parse(album_date_string).date()
        album = AlbumItem()
        album['date'] = album_date
        album['artist'] = artist
        album['mbid'] = mb_album['id']
        album['name'] = mb_album['title']
        album['popularity'] = sp_album.get('popularity', 0.0) / 100.0
        album['spotify_id'] = sp_album.get('id', '')
        album['spotify_url'] = sp_album.get('external_urls', {}) \
                                       .get('spotify', '')
        album['image'] = album_image

        album_score_sel = response.css('.metascore_w span::text')
        album_score = self.safe_extract(album_score_sel, default='0')
        album['score'] = album_score
        album['score_url'] = response.url

        album_summary_sel = response.css(
            '.summary_detail.product_summary span.data span::text'
        )
        album_summary = self.safe_extract(album_summary_sel)
        album['summary'] = album_summary

        album_tags_sel = response.css(
            'li.summary_detail.product_genre span.data::text'
        ).extract()
        album['tags'] = [genre.lower() for genre in sp_album.get('genres', [])]
        if not album['tags']:
            album['tags'] = [MusicHelper.clean_tag(tag) for tag in album_tags_sel]

        album_tracks = self.apis.mb_get_album_tracks(mb_release)
        spotify_track_items = sp_album.get('tracks', {}).get('items', [])
        if not spotify_track_items:
            self.logger.info('METACRITIC: skipping {0}-{1} due to missing spotify track info'.format(artist['name'], album['name']))
            return

        spotify_track_ids = [s_track.get('id') for s_track in spotify_track_items]
        self.logger.info('METACRITIC: track-ids {0}'.format(spotify_track_ids))
        if not spotify_track_ids:
            self.logger.info('METACRITIC: skipping {0}-{1} due to empty spotify track ids'.format(artist['name'], album['name']))
            return

        spotify_tracks = self.apis.spotify.tracks(spotify_track_ids).get('tracks', {})
        if not spotify_tracks:
            self.logger.info('METACRITIC: skipping {0}-{1} due to missing spotify track info'.format(artist['name'], album['name']))
            return

        spotify_track_features = self.apis.spotify.audio_features(tracks=[track.get('id', '') for track in spotify_tracks])
        spotify_len = len(spotify_tracks)
        tracks_list = []
        for i, t in enumerate(album_tracks):
            track = TrackItem()
            recording = t.get('recording', {})
            track['mbid'] = recording.get('id', '')
            track['name'] = recording.get('title', '')
            track['duration'] = recording.get('duration', 0)
            sonic = SonicInfoItem()
            if i < spotify_len:
                s_track = spotify_tracks[i]
                if fuzz.token_sort_ratio(track['name'], s_track.get('name', '')) < 40:
                    self.logger.info('METACRITIC: skipping track due to name mismatch')
                    continue

                track['track_number'] = s_track['track_number']
                track['popularity'] = s_track.get('popularity', 0.0) / 100.0
                track['duration'] = s_track.get('duration_ms', 0)
                track['spotify_url'] = s_track.get('external_urls', {}) \
                                              .get('spotify', '')
                track['spotify_id'] = s_track.get('id', '')
                ts = spotify_track_features[i]
                if not ts:
                    self.logger.info('METACRITIC: skipping {0}-{1}-{2} due to missing sonic info'.format(artist['name'], album['name'], track['name']))
                    continue
                sonic['acousticness'] = ts.get('acousticness', 0)
                sonic['danceability'] = ts.get('danceability', 0)
                sonic['energy'] = ts.get('energy', 0)
                sonic['instrumentalness'] = ts.get('instrumentalness', 0)
                sonic['liveness'] = ts.get('liveness', 0)
                sonic['loudness'] = ts.get('loudness', 0)
                sonic['speechiness'] = ts.get('speechiness', 0)
                sonic['tempo'] = ts.get('tempo', 0)
                sonic['valence'] = ts.get('valence', 0)
                sonic['mode'] = ts['mode']
                track['sonic_info'] = sonic
                tracks_list.append(track)
        album['tracks'] = tracks_list

        see_all_reviews = self.safe_extract(
            response.css('.reviews_module .see_all a::attr(href)'),
            default=None
        )
        if see_all_reviews:
            absolute_url = self.base_url + see_all_reviews
            request = scrapy.Request(
                absolute_url,
                callback=self.parse_all_reviews_page
            )
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
            publisher = PublisherItem()
            publisher['name'] = self.safe_extract(r.css('.source a::text'))

            review = ReviewItem()
            review['publisher'] = publisher
            review['score'] = self.safe_extract(
                r.css('.review_grade div::text'), default='0'
            )
            review['summary'] = self.safe_extract(
                r.css('.review_body::text')
            ).replace('\n', '').strip()

            rev_date = self.safe_extract(r.css('.date::text'))
            if rev_date:
                try:
                    review['date'] = dateparser.parse(rev_date).date()
                except:
                    self.logger.info('METACRITIC: invalid date in review {0}'.format(rev_date))

            rev_url = self.safe_extract(r.css('a.external::attr(href)'))
            if rev_url and rev_url != '://':
                publisher['url'] = self.parse_base_url(rev_url)
                review['url'] = rev_url
                review_list.append(review)

        return review_list



