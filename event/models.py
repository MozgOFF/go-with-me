from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    event_title = models.CharField(verbose_name="Event title", max_length=32)
    event_brief_description = models.CharField(verbose_name="Brief description", max_length=64)
    event_date = models.DateTimeField(verbose_name="Event date and time", null=False, default=datetime.now)
    EVENT_TYPES = (
        (1, "Charity"),
        (2, "Party"),
        (3, "Exhibition"),
        (4, "Concert"),
        (5, "Movie"),
        (6, "Theatre"),
        (7, "Meeting"),
        (8, "Education"),
        (9, "Business"),
        (10, "Entertainment"),
        (11, "Children"),
        (12, "Other"),
    )
    EVENT_STATES = (
        (1, "Active"),
        (2, "Inactive"),
        (3, "Moderating"),
        (4, "Archived"),
    )
    # event_ = models.ForeignKey()
    event_state = models.IntegerField(verbose_name="Event state", choices=EVENT_STATES)
    event_type = models.IntegerField(verbose_name="Event type", choices=EVENT_TYPES, default=3)
    event_user = models.ForeignKey(User, verbose_name="Event user", on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)