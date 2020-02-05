from django.conf.urls import include, url
from catalog import views as catalog_views


app_name = 'api'

urlpatterns = [
    url(
        regex=r'^albums/$',
        view=catalog_views.AlbumList.as_view(),
        name='album-list'
    ),
    url(
        regex=r'^artists/$',
        view=catalog_views.ArtistList.as_view(),
        name='artist-list'
    ),
    url(
        regex=r'^images/$',
        view=catalog_views.ImageList.as_view(),
        name='image-list'
    ),
    url(
        regex=r'^publishers/$',
        view=catalog_views.PublisherList.as_view(),
        name='publisher-list'
    ),
    url(
        regex=r'^reviews/$',
        view=catalog_views.ReviewList.as_view(),
        name='review-list'
    ),
    url(
        regex=r'^tracks/$',
        view=catalog_views.TrackList.as_view(),
        name='track-list'
    ),
]

