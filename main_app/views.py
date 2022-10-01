from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class Home(TemplateView):
    template_name = 'main_app/home.html'

class Signup(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'registration/signup.html'
