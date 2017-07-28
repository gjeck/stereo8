from django.conf.urls import include, url
from base import views as base_views

urlpatterns = [
    url(
        regex=r'^albums/$',
        view=base_views.AlbumList.as_view(),
        name='album-list'
    ),
    url(
        regex=r'^search/$',
        view=base_views.SearchViewSet.as_view(),
        name='search'
    ),
    url(
        regex=r'^autosearch/$',
        view=base_views.AutoSearchViewSet.as_view(),
        name='autosearch'
    ),
    url(
        regex=r'^artists/$',
        view=base_views.ArtistList.as_view(),
        name='artist-list'
    ),
    url(
        regex=r'^images/$',
        view=base_views.ImageList.as_view(),
        name='image-list'
    ),
    url(
        regex=r'^publishers/$',
        view=base_views.PublisherList.as_view(),
        name='publisher-list'
    ),
    url(
        regex=r'^reviews/$',
        view=base_views.ReviewList.as_view(),
        name='review-list'
    ),
    url(
        regex=r'^tracks/$',
        view=base_views.TrackList.as_view(),
        name='track-list'
    ),
]

