from django.contrib import admin
from .models import Category, Event, SubscriptionOnEvent

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(SubscriptionOnEvent)
