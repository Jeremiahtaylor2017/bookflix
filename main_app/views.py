from os import environ
from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.core import serializers
from .models import Album
from .forms import CreateUserForm, CreateAlbumForm, AlbumSearch

import environ
env = environ.Env()
environ.Env.read_env()


# Create your views here.
class Home(TemplateView):
    template_name = 'main_app/home.html'

    def get(self, request, *args, **kwargs):
        data = {}
        form = AlbumSearch(request.GET)

        if form.is_valid():
            data = form.get_album()
            if ('error' in data):
                messages.error(request, 'No album found')
                return render(request, self.template_name, {'form': form})

        else:
            form = AlbumSearch()

        new_album = Album()

        for key, value in data.items():
            for k, v in value.items():
                if k == 'name':
                    new_album.title = v
                if k == 'artist':
                    new_album.artist = v
                if k == 'image':
                    for index, item in enumerate(v):
                        if index == 2:
                            new_album.photo_url = item['#text']
                if k == 'wiki':
                    for ke, val in v.items():
                        if ke == 'published':
                            new_album.publish_date = val
                        if ke == 'summary':
                            new_album.summary = val
                if k == 'tags':
                    for ke, val in v.items():
                        for index, item in enumerate(val):
                            if index == 0:
                                print(item['name'])
                                new_album.genre = item['name']
                if k == 'tracks':
                    new_album.track_list = []
                    for ke, val in v.items():
                        for index, name in enumerate(val):
                            new_album.track_list.append(name['name'])
                            # print(name['name'])
                        # print(val)
                    # print(v)
                # print(k, v)
        # print(new_album.track_list)
        new_album.save()
        return render(request, self.template_name, {'form': form, 'data': data})



class Signup(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class ShowAlbumDetails(TemplateView):
    template_name = 'main_app/details.html'


class Index(TemplateView):
    template_name = 'main_app/index.html'

    def get(self, request):
        user_data = serializers.serialize("python", Album.objects.filter(profile=request.user.profile))
        data = serializers.serialize("python",Album.objects.all()) 
        return render(request, self.template_name, {'data': data, 'user_data': user_data})

class MyAlbums(TemplateView):
    template_name = 'main_app/my_albums.html'

    def get(self, request):
        data = serializers.serialize("python", Album.objects.filter(profile=request.user.profile))
        return render(request, self.template_name, {'data': data})


class DeleteAlbum(DeleteView):
    model = Album
    success_url = '/my_albums/'
    
    def get_context_data(self, **kwargs):
        id_int = int(self.request.path.split("/")[-1])
        id_str = self.request.path.split("/")[-1].split(" by ")[0]
        context = super().get_context_data(**kwargs)
        data = serializers.serialize("python", Album.objects.all())
        for obj in data:
            if obj["pk"] == id_int:
                context['album_cover'] = obj["fields"]["photo_url"]
            elif obj["fields"]["title"] == id_str:
                context['album_cover'] = obj["fields"]["photo_url"]
                
        return context
    

class CreateAlbum(CreateView):
    model = Album
    fields = '__all__'