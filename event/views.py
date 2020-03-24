from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from event.serializers import EventCreateSerializer, EventDetailSerializer
from .models import Event


class EventCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventCreateSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventDetailSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventDetailSerializer


# class EventDetailUpdate(generics.UpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = EventDetailSerializer


# class EventArchive(generics.UpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = EventArchiveSerializer
