from django import forms
from grunge.models import Playlist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'tracks']
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}), 
            'tracks': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
