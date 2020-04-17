from django.contrib import admin
from .models import EventImage, UserImages


@admin.register(EventImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'description', 'event', 'author', 'created', 'updated']
    list_filter = ['updated']


@admin.register(UserImages)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'description', 'user', 'created', 'updated']
    list_filter = ['updated']
