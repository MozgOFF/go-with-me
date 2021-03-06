from django.core.exceptions import ImproperlyConfigured
from rest_framework import response, decorators, permissions, status, viewsets, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserCreateSerializer,
    PasswordChangeSerializer,
    EmptySerializer,
    CheckPhoneSerializer,
    SMSMessageSerializer,
    ConfirmPhoneSerializer,
    ProfileInfoSerializer,
    RecoveryCheckPhoneSerializer,
)
from event.serializers import (
    EventListSerializer,
)
from .models import SMSMessage, Friendships
from event.models import Event
from django.shortcuts import get_object_or_404
import requests

User = get_user_model()

success_data = {'message': 'success'}


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = EmptySerializer
    serializer_classes = {
        'register': UserCreateSerializer,
        'password_change': PasswordChangeSerializer,
        'check_phone': CheckPhoneSerializer,
        'recovery_check_phone': RecoveryCheckPhoneSerializer,
        'confirm_phone': ConfirmPhoneSerializer,
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @decorators.action(methods=['POST'], detail=False, permission_classes=[permissions.AllowAny, ])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response.Response(res, status.HTTP_201_CREATED)

    @decorators.action(methods=['POST'], detail=False)
    def password_change(self, request):

        serializer = self.get_serializer(data=request.data)
        print("&&&check_phone serializer", serializer)

        if not serializer.is_valid():
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        request.user.set_password(serializer.validated_data['password'])
        request.user.save()

        return response.Response(data=success_data, status=status.HTTP_200_OK)

    @decorators.action(methods=['POST'], detail=False, permission_classes=[permissions.AllowAny, ])
    def recovery_check_phone(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        code = serializer.save()
        url = 'https://api.mobizon.kz/service/message/sendsmsmessage?recipient={0}&text={1}&apiKey=kzbf26cefde446a93ae901849e1ca7c3a430454bc3e5042a41e9f6720c0ac15f36b708'.format(
            request.data.get('phone'), code)
        response1 = requests.get(url)

        smsMessage = SMSMessage(content="Code {}".format(code))
        res = SMSMessageSerializer(smsMessage)

        return response.Response(res.data, status.HTTP_200_OK)

    @decorators.action(methods=['POST'], detail=False, permission_classes=[permissions.AllowAny, ])
    def check_phone(self, request):
        serializer = self.get_serializer(data=request.data)
        print("&&&check_phone serializer", serializer)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        print("asdasd", request.data.get('phone'))
        code = serializer.save()
        url = 'https://api.mobizon.kz/service/message/sendsmsmessage?recipient={0}&text={1}&apiKey=kzbf26cefde446a93ae901849e1ca7c3a430454bc3e5042a41e9f6720c0ac15f36b708'.format(
            request.data.get('phone'), code)
        response1 = requests.get(url)

        smsMessage = SMSMessage(content="Code {}".format(code))
        res = SMSMessageSerializer(smsMessage)

        return response.Response(res.data, status.HTTP_200_OK)

    @decorators.action(methods=['POST'], detail=False, permission_classes=[permissions.AllowAny, ])
    def confirm_phone(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return response.Response(data=success_data, status=status.HTTP_200_OK)


class MyInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProfileInfoSerializer

    def get(self, request, *args, **kwargs):
        user = ProfileInfoSerializer(request.user)
        return response.Response(data=user.data)


class MyFollowingView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileInfoSerializer

    def get_queryset(self):
        # Взять всех пользователей у кого я подписчик (тоесть мои подписки)
        query_set = User.objects.filter(followers=self.request.user)
        return query_set


class MyFollowersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileInfoSerializer

    def get_queryset(self):
        # Взять всех пользователей кто на подписан на меня (тоесть мои подписчики)
        query_set = User.objects.filter(following=self.request.user)
        return query_set


class FollowingView(generics.ListAPIView):
    serializer_class = ProfileInfoSerializer

    def get_queryset(self):
        # Взять всех пользователей у кого я подписчик (тоесть мои подписки)'
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        query_set = User.objects.filter(followers=user)
        return query_set


class FollowersView(generics.ListAPIView):
    serializer_class = ProfileInfoSerializer

    def get_queryset(self):
        # Взять всех пользователей кто на подписан на меня (тоесть мои подписчики)
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        query_set = User.objects.filter(following=user)
        return query_set


class MyEventsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventListSerializer

    def get_queryset(self):
        return self.request.user.event_set.get_queryset()


class FollowingEventsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventListSerializer

    def get_queryset(self):
        request = self.request
        query_set_followers = User.objects.filter(followers=request.user)
        query_set = Event.objects.filter(author__in=query_set_followers, status=2)
        return query_set


class ProfileDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.filter()
    serializer_class = ProfileInfoSerializer


class SubscribeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs.get('pk'))
        Friendships(from_user=request.user, to_user=user).save()
        # request.user.following.add(user)
        return response.Response(data=success_data, status=status.HTTP_200_OK)


class UnSubscribeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs.get('pk'))
        friendship = Friendships.objects.filter(from_user=request.user, to_user=user)
        friendship.delete()
        # request.user.following.remove(user)
        return response.Response(data=success_data, status=status.HTTP_200_OK)


class ViewedEventsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventListSerializer

    def get_queryset(self):
        return self.request.user.viewed_events.all().order_by('updated')


class SavedEventsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventListSerializer

    def get_queryset(self):
        return self.request.user.saved_events.all()


class UserEventsView(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return user.event_set.filter(status=2)
