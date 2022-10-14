from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import requests

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class AlbumSearch(forms.Form):
    artist = forms.CharField(label='artist', max_length=50)
    album = forms.CharField(label='album', max_length=50)

    def get_album(self):
        artist = self.cleaned_data.get('artist')
        album = self.cleaned_data.get('album')
        URL = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=36de190ae228eb292cedfc1fd10c5f38&artist={artist}&album={album}&format=json"
        response = requests.get(URL)
        data = response.json()
        return data