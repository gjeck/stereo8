import os
import re
import musicbrainzngs
import pylast
import pyen
import spotipy
import logging
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
        ''' Gets a musicbrainzngs release group by id
        Args:
            id: the musicbrainzngs id
        Returns:
            list of album releases
        '''
        return musicbrainzngs.get_release_group_by_id(id, 'releases')

    def mb_get_album_tracks(self, album):
        ''' Gets a list of tracks for a musicbrainzngs release-group
        Args:
            album: a musicbrainzngs release group dict
        Returns:
            list of musicbrainzngs tracks
        '''
        release = album.get('release-group', {}).get('release-list', [{}])[0]
        release_id = release.get('id', '')
        return musicbrainzngs.get_release_by_id(release_id, 'recordings') \
                             .get('release', {}) \
                             .get('medium-list', [{}])[0] \
                             .get('track-list', [{}])

    def sp_find_album(self, name, artist=''):
        ''' Searches and returns a spotify album
        Args:
            name: the album name
            artist: the album artist
        Return:
           dict of spotify album (or empty)
        '''
        query = 'album:{0} artist:{1}'.format(
            name.encode('utf-8'),
            artist.encode('utf-8')
        )
        try:
            response = self.spotify.search(query, type='album', limit=1)
            album_id = response.get('albums', {}) \
                               .get('items', [{}])[0] \
                               .get('id', '')
            return self.spotify.album(album_id)
        except Exception as e:
            logging.info('SPOTIFY: album not found {0}'.format(e))
            return {}

    def en_get_artist_familiarity(self, mbid):
        ''' Gets an echo nest artist familiarity
        Args:
            mbid: musicbrainzngs artist id
        Returns:
            float or 0.0
        '''
        return self.en_get_artist_property('familiarity', mbid)

    def en_get_artist_trending(self, mbid):
        ''' Gets an echo nest artist trending
        Args:
            mbid: musicbrainzngs artist id
        Returns:
            float or 0.0
        '''
        return self.en_get_artist_property('hotttnesss', mbid)

    def en_get_track_summary(self, mbid):
        ''' Gets the echo nest track summary (audio info)
        Args:
            mbid: musicbrainzngs track id
        Returns:
            dict of audio info or empty
        '''
        track_id = 'spotify:track:{0}'.format(mbid)
        try:
            response = self.en.get(
                'track/profile',
                id=track_id,
                bucket=['audio_summary']
            )
            return response.get('track', {}) \
                           .get('audio_summary', {})
        except Exception as e:
            logging.info('ECHO NEST: no summary for track {0}'.format(e))
            return {}
    
    def en_get_artist_property(self, path, mbid):
        ''' Gets an artist property endpoint from echo nest
        Args:
            path: the echo nest api endpoint
            mbid: musicbrainzngs artist id
        Returns:
            float of 0.0
        '''
        artist_id = 'musicbrainz:artist:{0}'.format(mbid)
        try:
            response = self.en.get('artist/{0}'.format(path), id=artist_id)
            return response.get('artist', {}) \
                           .get(path, 0)
        except Exception as e:
            logging.info('ECHO NEST: no artist property {0}'.format(e))
            return 0

    @staticmethod
    def build():
        ''' Builds a MusicHelper instance with api objects instantiated
        '''
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

