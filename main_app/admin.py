from django.contrib import admin

# Register your models here.
from .models import Profile, Album

admin.site.register(Profile)
admin.site.register(Album)