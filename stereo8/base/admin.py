from django.contrib import admin
from .models import (
    Album,
    Artist,
    Image,
    Publisher,
    Review,
    Track,
)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_artist')

    def get_artist(self, obj):
        return obj.artist.name

    get_artist.admin_order_field = 'artist__name'
    get_artist.short_description = 'Artist'


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'familiarity', 'trending')


class ImageAdmin(admin.ModelAdmin):
    list_display = ['mbid']


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_album', 'get_publisher', 'score')

    def get_album(self, obj):
        return obj.album.name 

    def get_publisher(self, obj):
        return obj.publisher.name

    get_album.admin_order_field = 'album__name'
    get_album.short_description = 'Album'
    get_publisher.admin_order_field = 'publisher__name'
    get_publisher.short_description = 'Publisher'


class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_album', 'get_artist')

    def get_album(self, obj):
        return obj.album.name 

    def get_artist(self, obj):
        return obj.album.artist.name

    get_album.admin_order_field = 'album__name'
    get_album.short_description = 'Album'
    get_artist.admin_order_field = 'album__artist__name'
    get_artist.short_description = 'Artist'
    

admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Track, TrackAdmin)
