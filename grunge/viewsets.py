from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .filters import AlbumFilter, ArtistFilter, TrackFilter
from .models import Album, Artist, Track , Playlist
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer , PlaylistSerializer
from rest_framework.response import Response
from rest_framework import status


class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilter


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")
    
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Playlist
from .serializers import PlaylistSerializer

class PlaylistAPIView(APIView):
    serializer_class = PlaylistSerializer
    
    def get_queryset(self):
        return Playlist.objects.all().prefetch_related('tracks')
    

    def post(self, request, *args, **kwargs):
        # Extract track IDs from request data
        track_ids = request.data.pop('tracks', [])

        serializer = PlaylistSerializer(data=request.data, context={'request': request})  # Pass the request object to the serializer context
        serializer.is_valid(raise_exception=True)
        playlist = serializer.save()

        # Add tracks to the playlist
        playlist.tracks.set(track_ids)

        # Serialize playlist with track details
        serialized_data = PlaylistSerializer(playlist, context={'request': request}).data  # Pass the request object to the serializer context

        return Response(serialized_data, status=status.HTTP_201_CREATED)


    
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        records_per_page = 8
        start_index = (page - 1) * records_per_page
        end_index = start_index + records_per_page

        queryset = Playlist.objects.all()[start_index:end_index]
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk=None , *args, **kwargs):
        queryset = self.get_queryset()
        playlist = get_object_or_404(queryset, pk=pk)

        serializer = PlaylistSerializer(playlist, data=request.data, context={'request': request})  # Pass the request object to the serializer context
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk=None , *args, **kwargs):
        return self.put(request, pk=pk)

    def delete(self, request, pk=None ,*args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=pk)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistDetailView(APIView):
    serializer_class = PlaylistSerializer

    def get_object(self, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
            return playlist
        except Playlist.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        playlist = self.get_object(pk)
        if not playlist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(playlist, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)