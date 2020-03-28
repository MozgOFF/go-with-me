from django.db import models
from django.contrib.auth import get_user_model
from event.models import Event

User = get_user_model()


class Comment(models.Model):
    content = models.TextField(verbose_name="Content")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
