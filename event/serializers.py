from rest_framework import serializers
from event.models import Event, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EventCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # categories = CategorySerializer(many=True)
    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'price', 'latitude', 'longitude', 'description', 'categories', 'author']

# class EventDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'


# class EventCreateSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Event
#         fields = '__all__'


# class EventUpdateDetailSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Event
#         fields = ('event_brief_description', 'event_title', 'event_date', 'event_type',)


# class EventArchiveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ('event_state',)
