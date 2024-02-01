from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet , PlaylistAPIView,PlaylistDetailView
from .views import artists
urlpatterns = []


if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns += [
        re_path("^$", RedirectView.as_view(url="/admin/", permanent=True)),
        path("admin/", admin.site.urls),
    ]

if settings.DJANGO_API_ENABLED:
    api_router = DefaultRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)
   

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
        
        path('playlists/', PlaylistAPIView.as_view(), name='playlist-list'),
        path('playlists/<int:pk>/', PlaylistAPIView.as_view(), name='playlist-detail'),
        path('playlist-detail/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail-api'),

        # Web Views 
        path("home/",  artists.home , name="home"),
        # Artist
        path("artists-view/",  artists.artists_view , name="artists-view"),
        path('artist-create/', artists.ArtistCreateView.as_view(), name='artist_create_view'),
        path('artist-update/<int:pk>/', artists.ArtistUpdateView.as_view(), name='artist_update_view'),
        
        # Albums
        path("albums-view/",  artists.albums_view , name="albums-view"),
        path('album-create/', artists.AlbumCreateView.as_view(), name='album_create_view'),
        path('album-update/<int:pk>/', artists.AlbumUpdateView.as_view(), name='album_update_view'),
        
        # Tracks
        path("tracks-view/",  artists.tracks_view , name="tracks-view"),
        path('track-create/', artists.TrackCreateView.as_view(), name='track_create_view'),
        path('track-update/<int:pk>/', artists.TrackUpdateView.as_view(), name='track_update_view'),

        # Playlist
        path("playlists-view/",  artists.playlists_view , name="playlist-view"),
        path('playlist-create-view/', artists.playlist_create_view, name='playlist_create_view'),
        path('playlist-update-view/<int:pk>/', artists.playlist_update_view, name='playlist_update_view'),
        path('playlists_delete_view/<int:pk>/', artists.playlists_delete_view, name='playlists_delete_view'),


    ]
