from django.db import models

from event.models import Event
from gowithme.settings import AUTH_USER_MODEL


class EventImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    event = models.ForeignKey(Event, related_name='images', blank=True, null=True, default=None, on_delete=models.CASCADE)
    author = models.ForeignKey(AUTH_USER_MODEL, related_name='event_images_uploaded', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}, {}.".format(self.id, self.description[:20])
