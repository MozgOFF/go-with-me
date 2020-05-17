from rest_framework import generics, views, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from event.serializers import EventCreateSerializer, EventDetailSerializer, EventListSerializer, CategorySerializer
from .models import Event, Category
from .filters import EventFilter
from comment.models import Comment
from comment.serializers import CommentSerializer
from account.serializers import ShortProfileInfoSerializer

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


class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', ]
    ordering_fields = ['start', 'view_counter', 'price', 'created']
    ordering = ['created']


class EventSubscribersView(generics.ListAPIView):
    serializer_class = ShortProfileInfoSerializer

    def get_queryset(self):
        return Event.objects.get(id=self.kwargs['pk']).subscribed_by.all()



class SpecialEventListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EventListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', ]
    ordering_fields = ['start', 'view_counter', 'price', 'created']
    ordering = ['created']

    def get_queryset(self):
        categories = self.request.user.favorite_category.all()
        events = Event.objects.filter(categories__in=categories)
        return events


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventDetailSerializer

    def get(self, request, *args, **kwargs):
        event = Event.objects.filter(id=kwargs['pk'])
        event.update(view_counter=F('view_counter') + 1)
        if request.user.id is not None:
            request.user.viewed_events.add(event.first())

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
        event_set = Event.objects.filter(id=pk)
        if event_set.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event = event_set.first()
        event.subscribed_by.add(request.user)

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


class EventCategoriesView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = None
