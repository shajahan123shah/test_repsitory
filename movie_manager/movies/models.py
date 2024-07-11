
from django.contrib.auth.models import User
from django.db import models

class CensorInfo(models.Model):
    rating = models.CharField(max_length=50)
    certified_by = models.CharField(max_length=50)

    def __str__(self):
        return self.certified_by

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MovieInfo(models.Model):
    title = models.CharField(max_length=250)
    year = models.IntegerField(null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    censor_info = models.OneToOneField(CensorInfo, on_delete=models.SET_NULL, null=True, related_name='movie')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies', default=1)
    actors = models.ManyToManyField(Actor, related_name='movies')

    def __str__(self):
        return self.title
    
    # models.py


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any additional fields you want for the profile
#     bio = models.TextField(blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True, null=True)
#     birth_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username

