from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from event.serializers import EventDetailSerializer, EventCreateSerializer, EventUpdateDetailSerializer, \
    EventArchiveSerializer
from .models import Event


class EventCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventCreateSerializer


class EventListView(generics.ListAPIView):
    serializer_class = EventDetailSerializer
    queryset = Event.objects.all()


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventDetailSerializer
    queryset = Event.objects.all()


class EventDetailUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventDetailSerializer


class EventArchive(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventArchiveSerializer
