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
    latitude = models.DecimalField(verbose_name="Latitude", max_digits=17, decimal_places=14)
    longitude = models.DecimalField(verbose_name="Longitude", max_digits=17, decimal_places=14)
    categories = models.ManyToManyField(Category, related_name="events")
    saved_by = models.ManyToManyField(User, related_name='saved_events', blank=True, related_query_name='saved_events')
    liked_by = models.ManyToManyField(User, related_name='liked_events', blank=True, related_query_name='liked_events')
    subscribed_by = models.ManyToManyField(User,
                                           through='SubscriptionOnEvent',
                                           related_name='subscribed_events',
                                           blank=True,
                                           related_query_name='subscribed_events')
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    view_counter = models.IntegerField(verbose_name='View counter', default=0)
    is_active = models.BooleanField(verbose_name="Is active", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


class SubscriptionOnEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_accepted_by_author = models.BooleanField(verbose_name="Is accepted by author of event", default=False)
