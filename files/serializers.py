from rest_framework import serializers

from files.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('created_at', 'image_file')
