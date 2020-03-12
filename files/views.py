from rest_framework import viewsets
from rest_framework import generics
from files.models import Image
from files.serializers import ImageSerializer


class ImageViewSet(generics.CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
