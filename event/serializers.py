from rest_framework import serializers
from event.models import Event, Category
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from comment.models import Comment
from comment.serializers import CommentSerializer
from files.models import EventImage
from account.serializers import ShortProfileInfoSerializer

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class EventImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id']


class EventCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'price', 'latitude', 'longitude', 'description', 'categories', 'author', 'images']


class EventImageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventImage
        fields = ['image', 'description']


class EventListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    is_saved = serializers.SerializerMethodField()
    author = ShortProfileInfoSerializer()
    images = serializers.SerializerMethodField()

    @staticmethod
    def get_images(obj):
        return EventImageSerializer(obj.images, many=True).data

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        if user.id is None:
            return False

        return obj in user.saved_events.get_queryset()

    class Meta:
        model = Event
        fields = ['id',
                  'title',
                  'start',
                  'end',
                  'price',
                  'latitude',
                  'longitude',
                  'description',
                  'categories',
                  'author',
                  'is_saved',
                  'view_counter',
                  'images']


class EventDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Event
        fields = ['id',
                  'title',
                  'start',
                  'end',
                  'price',
                  'latitude',
                  'longitude',
                  'description',
                  'categories',
                  'author',
                  'view_counter']


class EventCommentsSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['comment_set', ]
