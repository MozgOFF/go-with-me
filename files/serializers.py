from rest_framework import serializers

from .models import EventImage, UserImages


class EventImageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EventImage
        fields = ['id', 'image', 'description', 'author']


class UserImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserImages
        fields = ['id', 'image', 'description', 'user']
