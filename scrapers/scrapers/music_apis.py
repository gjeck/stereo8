import os, musicbrainzngs, pyen, pylast


class MusicHelper():

    def __init__(self):
        musicbrainzngs.set_useragent('Stereo8', '0.1.0', 'https://github.com/gjeck/stereo8')
        self.echoen = pyen.Pyen()
        lastfm_api_key = os.environ.get('LAST_FM_API_KEY', '')
        lastfm_api_secret = os.environ.get('LAST_FM_API_SECRET', '')
        lastfm = pylast.LastFMNetwork(api_key=lastfm_api_key, api_secret=lastfm_api_secret)

    def mb_find_album(self, name, artist):
        response = musicbrainzngs.search_release_groups(query=name, artist=artist, limit=1)
        release_list = response['release-group-list']
        return release_list[0]
