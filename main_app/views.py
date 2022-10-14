from os import environ

from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.core import serializers

from .models import Album
from .forms import CreateUserForm, AlbumSearch

import environ
env = environ.Env()
environ.Env.read_env()


# Create your views here.
class Home(TemplateView):
    template_name = 'main_app/home.html'

    def get(self, request):
        data = {}
        if 'artist' and 'album' in request.GET:
            form = AlbumSearch(request.GET)
            if form.is_valid():
                data = form.get_album()
        else:
            form = AlbumSearch()

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

