from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('albums/details/', views.ShowBook.as_view()),
    path('accounts/signup/', views.Signup.as_view(), name='signup')
]
