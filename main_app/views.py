from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import requests

API_KEY = '36de190ae228eb292cedfc1fd10c5f38'

# Create your views here.
class Home(TemplateView):
    template_name = 'main_app/home.html'

class Signup(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)



class ShowBook(TemplateView):
    template_name = 'main_app/home.html'

    def get(self, request):
        URL = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=36de190ae228eb292cedfc1fd10c5f38&artist=Drake&album=Thank%20Me%20Later&format=json'
        response = requests.get(URL)
        data = response.json()
        return render(request, self.template_name, {'data': data})



