from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.models import Event, ClientTickets


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_name', 'pictures', 'event_date', 'city', 'country']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTickets
        fields = ['id', 'names', 'amount', 'bought_date', 'used']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTickets
        fields = '__all__'


class EventKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['eventkeys']
