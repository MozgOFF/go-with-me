# from rest_framework import serializers
# from event.models import Event


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
