from django.db import models
from accounts.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_text = models.TextField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.user.username


class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    film = models.ForeignKey('movies.FilmWork', on_delete=models.CASCADE)

    def __str__(self):
        return self.profile + " - " + self.film.name