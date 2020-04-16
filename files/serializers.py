from rest_framework import serializers

from .models import EventImage


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EventImage
        fields = ['id', 'image', 'description', 'author']
