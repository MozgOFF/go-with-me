from rest_framework import generics, views, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from event.serializers import EventCreateSerializer, EventDetailSerializer, EventListSerializer
from .models import Event
from .filters import EventFilter
from comment.models import Comment
from comment.serializers import CommentSerializer
from event.tasks import h
from datetime import datetime, timedelta

success_data = {'message': 'success'}


class EventFilteredView:
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', ]
    ordering_fields = ['start', 'view_counter', 'price', 'created']
    ordering = ['created']


class EventCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventCreateSerializer

    def create(self, request, *args, **kwargs):
        print("EventCreateView create")
        a = h.delay(2, 5)
        print("EventCreateView create ", a.status)
        return super(EventCreateView, self).create(request)


class EventListView(generics.ListAPIView, EventFilteredView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        print("EventListView list()")
        t = datetime.utcnow() + timedelta(seconds=10)
        task = h.apply_async(eta=t)
        print(f"id={task.id}, state={task.state}, status={task.status}")

        return super(EventListView, self).list(request)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventDetailSerializer

    def get(self, request, *args, **kwargs):
        Event.objects.filter(id=kwargs['pk']).update(view_counter=F('view_counter') + 1)
        return super(EventDetailView, self).get(request)


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

        return Response(data=success_data, status=status.HTTP_200_OK)


class RemoveEventView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event.first().saved_by.remove(request.user)
        return Response(data=success_data, status=status.HTTP_200_OK)


class LikeEventView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event.first().liked_by.add(request.user)
        return Response(data=success_data, status=status.HTTP_200_OK)


class UnlikeEventView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event.first().liked_by.remove(request.user)
        return Response(data=success_data, status=status.HTTP_200_OK)


class SubscribeOnEventView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event.first().subscribed_by.add(request.user)
        # TODO notify author
        return Response(data=success_data, status=status.HTTP_200_OK)


class UnsubscribeFromEventView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        event = Event.objects.filter(id=pk)
        if event.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event.first().subscribed_by.remove(request.user)
        return Response(data=success_data, status=status.HTTP_200_OK)
