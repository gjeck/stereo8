import os
import re
import musicbrainzngs
import pylast
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging
from django.utils.html import strip_tags


class MusicHelper():

    def __init__(self, spotify, lastfm):
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
        query = 'album:{0} artist:{1}'.format(name, artist)
        try:
            response = self.spotify.search(query, type='album', limit=1)
            album_id = response.get('albums', {}) \
                               .get('items', [{}])[0] \
                               .get('id', '')
            return self.spotify.album(album_id)
        except Exception as e:
            logging.info('SPOTIFY: album not found {0}'.format(e))
            return None

    def sp_find_artist(self, artist_name):
        query = 'artist:{0}'.format(artist_name)
        try:
            response = self.spotify.search(query, type='artist', limit=1)
            artist_id = response.get('artists', {}) \
                                .get('items', [{}])[0] \
                                .get('id', '')
            return self.spotify.artist(artist_id)
        except Exception as e:
            logging.info('SPOTIFY: artist not found {0}'.format(e))
            return None

    @staticmethod
    def build():
        ''' Builds a MusicHelper instance with api objects instantiated
        '''
        musicbrainzngs.set_useragent(
            'Stereo8',
            '0.1.0',
            'https://github.com/gjeck/stereo8'
        )
        client_credentials_manager = SpotifyClientCredentials()
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        lastfm = pylast.LastFMNetwork(
            api_key=os.environ.get('LAST_FM_API_KEY', ''),
            api_secret=os.environ.get('LAST_FM_API_SECRET', '')
        )
        lastfm.enable_rate_limit()
        lastfm.enable_caching()
        return MusicHelper(spotify, lastfm)

    @staticmethod
    def lastfm_clean_summary(summary):
        clean_summary = MusicHelper.rchop(strip_tags(summary.replace('\n', '').strip()), "Read more on Last.fm")
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

    @staticmethod
    def rchop(thestring, ending):
        ''' Chops the end off a string if the end matches a substring
        Args:
            thestring: the string to chop
            ending: the substring to match
        Returns:
            the input string minus the matched end
        '''
        if thestring.endswith(ending):
            return thestring[:-len(ending)]
        return thestring

