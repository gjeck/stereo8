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
                'familiarity': item['artist']['familiarity'],
                'image': artist_image,
                'name': item['artist']['name'],
                'trending': item['artist']['trending'],
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
                    'date': r['date'],
                    'score': r['score'],
                    'summary': r['summary'],
                }
            )

        for t in item['tracks']:
            sonic, created = SonicInfo.objects.update_or_create(
                mbid=t['mbid'],
                defaults={
                    'acousticness': t['sonic_info']['acousticness'],
                    'danceability': t['sonic_info']['danceability'],
                    'energy': t['sonic_info']['energy'],
                    'instrumentalness': t['sonic_info']['instrumentalness'],
                    'liveness': t['sonic_info']['liveness'],
                    'loudness': t['sonic_info']['loudness'],
                    'speechiness': t['sonic_info']['speechiness'],
                    'tempo': t['sonic_info']['tempo'],
                    'valence': t['sonic_info']['valence'],
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

