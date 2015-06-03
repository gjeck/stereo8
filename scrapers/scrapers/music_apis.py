import os
import re
import musicbrainzngs
import pylast
import pyen
import spotipy
from django.utils.html import strip_tags


class MusicHelper():

    def __init__(self, en, spotify, lastfm):
        self.en = en
        self.spotify = spotify
        self.lastfm = lastfm

    def mb_find_album(self, name, artist=''):
        ''' Searches musicbrainzngs release groups and returns the first result
        Args:
            name: the album name
            artist: the artist name
        Returns:
            dict with first result
        '''
        response = musicbrainzngs.search_release_groups(
            query=name,
            artist=artist,
            limit=1
        )
        return response.get('release-group-list', [None])[0]

    def mb_get_album_by_id(self, id):
        return musicbrainzngs.get_release_group_by_id(id, 'releases')

    def mb_get_album_tracks(self, album):
        release = album.get('release-group', {}).get('release-list', [{}])[0]
        release_id = release.get('id', '')
        return musicbrainzngs.get_release_by_id(release_id, 'recordings') \
                             .get('release', {}) \
                             .get('medium-list', [{}])[0] \
                             .get('track-list', [{}])

    def sp_find_album(self, name, artist=''):
        query = 'album:{0} artist:{1}'.format(
            name.encode('utf-8'),
            artist.encode('utf-8')
        )
        response = self.spotify.search(query, type='album', limit=1)
        album_items = response.get('albums', {}) \
                           .get('items', [])
        if album_items:
            album_id = album_items[0].get('id', '')
            return self.spotify.album(album_id)
        else:
            return {}

    def en_get_artist_familiarity(self, mbid):
        artist_id = 'musicbrainz:artist:{0}'.format(mbid)
        response = self.en.get('artist/familiarity', id=artist_id)
        return response.get('artist', {}) \
                       .get('familiarity', 0)

    def en_get_artist_trending(self, mbid):
        artist_id = 'musicbrainz:artist:{0}'.format(mbid)
        response = self.en.get('artist/hotttnesss', id=artist_id)
        return response.get('artist', {}) \
                       .get('hotttnesss', 0)

    @staticmethod
    def build():
        musicbrainzngs.set_useragent(
            'Stereo8',
            '0.1.0',
            'https://github.com/gjeck/stereo8'
        )
        en = pyen.Pyen()
        spotify = spotipy.Spotify()
        lastfm = pylast.LastFMNetwork(
            api_key=os.environ.get('LAST_FM_API_KEY', ''),
            api_secret=os.environ.get('LAST_FM_API_SECRET', '')
        )
        lastfm.enable_rate_limit()
        lastfm.enable_caching()
        return MusicHelper(en, spotify, lastfm)

    @staticmethod
    def lastfm_clean_summary(summary):
        clean_summary = strip_tags(summary.replace('\n', '').strip())
        final = re.split(r'\s{4,}', clean_summary)
        if final:
            return final[0]
        else:
            return clean_summary

    @staticmethod
    def lastfm_clean_tag(tag):
        return re.sub(r'-|\/', ' ', tag.item.get_name().lower())

    @staticmethod
    def clean_tag(tag):
        return re.sub(r'-|\/', ' ', tag.lower())

