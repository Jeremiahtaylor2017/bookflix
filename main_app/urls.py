from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('albums/details/', views.ShowBook.as_view()),
    path('albums/details/ShowAlbumDetails', views.ShowAlbumDetails.as_view(), name='album_details'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
    path('index/', views.Index.as_view(), name='index'),
    path('my_albums/', views.MyAlbums.as_view(), name='my_albums'),
    path('my_albums/delete/<int:pk>', views.DeleteAlbum.as_view(), name='delete_album')
]
