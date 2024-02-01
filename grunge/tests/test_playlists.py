from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from grunge.models import Playlist

class PlaylistAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.playlist_data = {
            'name': 'Test Playlist',
            'tracks': []  # You can provide track IDs here
        }
        self.playlist = Playlist.objects.create(name='Existing Playlist')

    def test_create_playlist(self):
        response = self.client.post('/playlists/', self.playlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_playlist(self):
        response = self.client.get(f'/playlists/{self.playlist.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_playlist(self):
        updated_data = {'name': 'Updated Playlist'}
        response = self.client.put(f'/playlists/{self.playlist.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_partial_update_playlist(self):
        updated_data = {'name': 'Updated Playlist'}
        response = self.client.patch(f'/playlists/{self.playlist.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_playlist(self):
        response = self.client.delete(f'/playlists/{self.playlist.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
