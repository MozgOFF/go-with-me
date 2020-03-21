from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    is_active = models.BooleanField(verbose_name="Is active")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

class Event(models.Model):
    title = models.CharField(verbose_name="Event title", max_length=256)
    description = models.CharField(verbose_name="Brief description", max_length=1024)
    start = models.DateTimeField(verbose_name="Event begining")
    end = models.DateTimeField(verbose_name="Event ending")
    price = models.CharField(verbose_name="Price", max_length=20) 
    latitude = models.DecimalField(verbose_name="Latitude", max_digits=10, decimal_places=7)
    longitude = models.DecimalField(verbose_name="Longitude", max_digits=10, decimal_places=7)
    categories = models.ManyToManyField(Category, related_name="events")
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is active", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
