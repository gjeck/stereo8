from scrapers.items import AlbumItem
from base.models import (
    Artist,
    Album,
    Image,
    Review,
    Publisher,
    Track,
    SonicInfo,
)


class DjangoItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AlbumItem):
            self.process_album(item, spider)

        return item

    def process_album(self, item, spider):
        artist_image, created = Image.objects.update_or_create(
            mbid=item['artist']['mbid'],
            defaults={
                'large': item['artist']['image']['large'],
                'medium': item['artist']['image']['medium'],
                'small': item['artist']['image']['small'],
            }
        )

        artist, created = Artist.objects.update_or_create(
            mbid=item['artist']['mbid'],
            defaults={
                'bio': item['artist']['bio'],
                'bio_url': item['artist']['bio_url'],
                'image': artist_image,
                'name': item['artist']['name'],
                'spotify_id': item['artist']['spotify_id'],
                'spotify_url': item['artist']['spotify_url'],
            }
        )
        artist.tags.add(*item['artist']['tags'])

        album_image, created = Image.objects.update_or_create(
            mbid=item['mbid'],
            defaults={
                'large': item['image']['large'],
                'medium': item['image']['medium'],
                'small': item['image']['small'],
            }
        )

        album, created = Album.objects.update_or_create(
            mbid=item['mbid'],
            defaults={
                'artist': artist,
                'date': item['date'],
                'image': album_image,
                'name': item['name'],
                'summary': item['summary'],
                'popularity': item['popularity'],
                'score': item['score'],
                'score_url': item['score_url'],
                'spotify_id': item['spotify_id'],
                'spotify_url': item['spotify_url'],
            }
        )
        album.tags.add(*item['tags'])

        for r in item['reviews']:
            publisher, created = Publisher.objects.update_or_create(
                url=r['publisher']['url'],
                defaults={
                    'name': r['publisher']['name'],
                }
            )

            review, created = Review.objects.update_or_create(
                url=r['url'],
                defaults={
                    'album': album,
                    'publisher': publisher,
                    'date': r.get('date', None),
                    'score': r['score'],
                    'summary': r['summary'],
                }
            )

        for t in item['tracks']:
            sonic, created = SonicInfo.objects.update_or_create(
                mbid=t['mbid'],
                defaults={
                    'acousticness': t['sonic_info'].get('acousticness', 0),
                    'danceability': t['sonic_info'].get('danceability', 0),
                    'energy': t['sonic_info'].get('energy', 0),
                    'instrumentalness': t['sonic_info'].get('instrumentalness', 0),
                    'liveness': t['sonic_info'].get('liveness', 0),
                    'loudness': t['sonic_info'].get('loudness', 0),
                    'speechiness': t['sonic_info'].get('speechiness', 0),
                    'tempo': t['sonic_info'].get('tempo', 0),
                    'valence': t['sonic_info'].get('valence', 0),
                    'mode': t['sonic_info'].get('mode', 0)
                }
            )
            track, created = Track.objects.update_or_create(
                mbid=t['mbid'],
                defaults={
                    'album': album,
                    'sonic_info': sonic,
                    'duration': t['duration'],
                    'name': t['name'],
                    'spotify_id': t['spotify_id'],
                    'spotify_url': t['spotify_url'],
                }
            )

        album.update_sonic_info()
        artist.update_sonic_info()

        return item

