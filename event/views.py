from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from event.serializers import EventCreateSerializer, EventDetailSerializer, EventListSerializer
from .models import Event
from comment.models import Comment
from comment.serializers import CommentSerializer


class EventCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventCreateSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListSerializer

    def list(self, request, *args, **kwargs):
        return super(EventListView, self).list(request)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventDetailSerializer


class EventCommentsView(generics.ListAPIView):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(event=kwargs.get('pk'))
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class SaveEventView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        event.first().saved_by.add(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveEventView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        event.first().saved_by.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
