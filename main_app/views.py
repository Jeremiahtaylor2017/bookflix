from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

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
