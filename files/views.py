from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from files.models import EventImage
from files.serializers import ImageSerializer


class EventImageUploadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ImageSerializer
    queryset = EventImage.objects.all()


class ImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer
    queryset = EventImage.objects.all()
