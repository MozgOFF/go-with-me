from django.contrib import admin
from .models import EventImage


@admin.register(EventImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'description', 'author', 'created', 'updated']
    list_filter = ['updated']
