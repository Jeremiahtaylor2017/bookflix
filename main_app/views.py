from operator import concat
from os import environ
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.template.defaulttags import register
from .models import Album
import requests

import environ
env = environ.Env()
environ.Env.read_env()

from .forms import CreateUserForm

# Create your views here.
class Home(TemplateView):
    template_name = 'main_app/home.html'

    def get(self, request):
        return redirect("accounts/login/")

class Signup(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    # form_class = UserCreationForm
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)



class ShowBook(TemplateView):
    template_name = 'main_app/home.html'

    def get(self, request):
        URL = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={env('API_KEY')}&artist=Drake&album=Thank%20Me%20Later&format=json"
        response = requests.get(URL)
        data = response.json()
        return render(request, self.template_name, {'data': data})

class ShowAlbumDetails(TemplateView):
    template_name = 'main_app/details.html'

    def get(self, request):
        URL = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={env('API_KEY')}&artist=Drake&album=Thank%20Me%20Later&format=json"
        response = requests.get(URL)
        data = response.json()
        return render(request, self.template_name, {'data': data})


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
        
        id_int = self.request.path.split("/")[-1]
        id_str = self.request.path.split("/")[-1].split(" by ")[0]
        
        context = super().get_context_data(**kwargs)
        data = serializers.serialize("python", Album.objects.all())


        for obj in data:
            if obj["pk"] == id_int:
                context['album_cover'] = obj["fields"]["photo_url"]
            elif obj["fields"]["title"] == id_str:
                context['album_cover'] = obj["fields"]["photo_url"]
        
        print(context)
        return context
    

    


