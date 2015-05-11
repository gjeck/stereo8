import os, re, musicbrainzngs, pylast


class MusicHelper():

    def __init__(self):
        musicbrainzngs.set_useragent('Stereo8', '0.1.0', 'https://github.com/gjeck/stereo8')
        lastfm_api_key = os.environ.get('LAST_FM_API_KEY', '')
        lastfm_api_secret = os.environ.get('LAST_FM_API_SECRET', '')
        self.lastfm = pylast.LastFMNetwork(api_key=lastfm_api_key, api_secret=lastfm_api_secret)
        self.lastfm.enable_rate_limit()
        self.lastfm.enable_caching()

    def mb_find_album(self, name, artist):
        ''' Searches musicbrainzngs release groups and returns the first result (best match)
        Args:
            name: the album name
            artist: the artist name
        Returns:
            dict with first result
        '''
        response = musicbrainzngs.search_release_groups(query=name, artist=artist, limit=1)
        release_list = response['release-group-list']
        return release_list[0]

    def lastfm_clean_summary(self, summary):
        return re.sub('<a.+?\/a>\.', summary).replace('\n', '').strip()

