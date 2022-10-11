from os import environ
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import requests

import environ
env = environ.Env()
environ.Env.read_env()

from .forms import CreateUserForm

# Create your views here.
class Home(TemplateView):
    template_name = 'main_app/home.html'

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



