from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from files.models import EventImage, UserImages
from files.serializers import EventImageSerializer, UserImageSerializer


class EventImageUploadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EventImageSerializer
    queryset = EventImage.objects.all()


class EventImageListView(generics.ListAPIView):
    serializer_class = EventImageSerializer
    queryset = EventImage.objects.all()


class UserImageUploadView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserImageSerializer
    queryset = UserImages.objects.all()