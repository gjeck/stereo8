import os, re, musicbrainzngs, pylast, pyen, spotipy
from django.utils.html import strip_tags


class MusicHelper():

    def __init__(self):
        musicbrainzngs.set_useragent('Stereo8', '0.1.0', 'https://github.com/gjeck/stereo8')
        self.en = pyen.Pyen()
        self.spotify = spotipy.Spotify()
        lastfm_api_key = os.environ.get('LAST_FM_API_KEY', '')
        lastfm_api_secret = os.environ.get('LAST_FM_API_SECRET', '')
        self.lastfm = pylast.LastFMNetwork(api_key=lastfm_api_key, api_secret=lastfm_api_secret)
        self.lastfm.enable_rate_limit()
        self.lastfm.enable_caching()

    def mb_find_album(self, name, artist=''):
        ''' Searches musicbrainzngs release groups and returns the first result (best match)
        Args:
            name: the album name
            artist: the artist name
        Returns:
            dict with first result
        '''
        response = musicbrainzngs.search_release_groups(query=name, artist=artist, limit=1)
        release_list = response['release-group-list']
        return release_list[0] if release_list else None

    def sp_find_album(self, name, artist=''):
        query = 'album:{0} artist:{1}'.format(name, artist)
        response = self.spotify.search(query, type='album', limit=1)
        response_album = response['albums']['items']
        if not response_album:
            return {}
        album_id = response['albums']['items'][0]['id']
        album = self.spotify.album(album_id)
        return album if album else {}

    def mb_get_album_by_id(self, id):
        return musicbrainzngs.get_release_group_by_id(id)

    def en_get_artist_familiarity(self, mbid):
        artist_id = 'musicbrainz:artist:{0}'.format(mbid)
        response = self.en.get('artist/familiarity', id=artist_id)
        if response:
            return response['artist']['familiarity']
        else:
            return None

    def en_get_artist_trending(self, mbid):
        artist_id = 'musicbrainz:artist:{0}'.format(mbid)
        response = self.en.get('artist/hotttnesss', id=artist_id)
        if response:
            return response['artist']['hotttnesss']
        else:
            return None

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

