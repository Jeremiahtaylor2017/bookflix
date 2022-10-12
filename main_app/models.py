from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    publish_date = models.DateField('publish date')
    genre = models.CharField(max_length=50)
    summary = models.TextField(max_length=500)
    track_list = ArrayField(models.CharField(max_length=50), null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.artist}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    albums = models.ManyToManyField(Album)

    def __str__(self):
        return f'{self.user}\'s albums'

"""
The functions below are the automatically create/update the Profile model
when the User instance is created or updated.
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




    

