from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login ,  logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from grunge.models import Album, Artist, Track , Playlist
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from grunge.forms.forms import PlaylistForm

def home(request):
    artists = Artist.objects.all().count()
    albums = Album.objects.all().count()
    tracks = Track.objects.all().count()
    return render(request , "home.html",locals() )

############# Artists View ####################
def artists_view(request):
    artist_list = Artist.objects.all()
    paginator = Paginator(artist_list, 10)  # 10 artists per page

    page_number = request.GET.get('page')
    artists = paginator.get_page(page_number)

    return render(request, "artists.html", {'artists': artists})


class ArtistCreateView(CreateView):
    model = Artist
    fields = ['name']
    template_name = 'form.html'  
    success_url = reverse_lazy('artists-view') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Artist created successfully!')
        return response


class ArtistUpdateView(UpdateView):
    model = Artist
    fields = ['name']
    template_name = 'form.html'  
    success_url = reverse_lazy('artists-view')  

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Artist updated successfully!')
        return response


#############  Albums Views #####################
def albums_view(request):
    album_list = Album.objects.all()
    paginator = Paginator(album_list, 10)  # 10 albums per page

    page_number = request.GET.get('page')
    albums = paginator.get_page(page_number)

    return render(request, "albums.html", {'albums': albums})

class AlbumCreateView(CreateView):
    model = Album
    fields = ['name','year','artist']
    template_name = 'form.html'  
    success_url = reverse_lazy('albums-view') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Album created successfully!')
        return response
    
class AlbumUpdateView(UpdateView):
    model = Album
    fields = ['name','year','artist']
    template_name = 'form.html'  
    success_url = reverse_lazy('albums-view') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Album updated successfully!')
        return response

##############   Tracks View ##############

def tracks_view(request):
    track_list = Track.objects.all().order_by('album')
    paginator = Paginator(track_list, 10)  # 10 tracks per page

    page_number = request.GET.get('page')
    tracks = paginator.get_page(page_number)

    return render(request, "tracks.html", {'tracks': tracks})


class TrackCreateView(CreateView):
    model = Track
    fields = ['name','number','album']
    template_name = 'form.html'  
    success_url = reverse_lazy('tracks-view') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Track created successfully!')
        return response
    
class TrackUpdateView(UpdateView):
    model = Track
    fields = ['name','number','album']
    template_name = 'form.html'  
    success_url = reverse_lazy('tracks-view') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Track updated successfully!')
        return response

##################  Playlist
def playlists_view(request):
    playlists_list = Playlist.objects.all()
    print(playlists_list)
    paginator = Paginator(playlists_list, 10)  # 10 tracks per page

    page_number = request.GET.get('page')
    playlists = paginator.get_page(page_number)

    return render(request, "playlist.html", {'playlists': playlists})

def playlists_delete_view(request ,pk):
    obj= Playlist.objects.get(id=pk)
    obj.delete()
    messages.success(request ,"Deleted Successfully")
    return redirect("playlist-view")


def playlist_create_view(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request ,"Playlist Added Successfully")
            return redirect('playlist-view')  # Redirect to the playlist view after successful creation
    else:
        form = PlaylistForm()
    return render(request, 'form.html', {'form': form})


def playlist_update_view(request , pk):
    obj = Playlist.objects.get(id=pk)
    if request.method == 'POST':
        form = PlaylistForm(request.POST , instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request ,"Playlist Update Successfully")
            return redirect('playlist-view')  # Redirect to the playlist view after successful creation
    else:
        form = PlaylistForm(instance=obj)
    return render(request, 'form.html', {'form': form})
