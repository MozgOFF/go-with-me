from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Location(models.Model):
    latitude = models.CharField(max_length=25)
    longitude = models.CharField(max_length=25)


class Event(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id', db_index=True, unique=True)
    title = models.CharField(verbose_name="Event title", max_length=256)
    description = models.CharField(verbose_name="Brief description", max_length=1024)
    start = models.DateTimeField(verbose_name="Event begining")
    end = models.DateTimeField(verbose_name="Event ending")
    price = models.CharField(verbose_name="Price", max_length=20)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    is_active = models.BooleanField(verbose_name="Is active")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
