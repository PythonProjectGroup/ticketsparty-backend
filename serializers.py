from rest_framework import serializers
from backend.models import Event, ClientTickets
from django.contrib.auth import get_user_model

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = '__all__'

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_name', 'event_date', 'city', 'country']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTickets
        fields = ['used', 'amount', 'id', 'client_id', 'event_id', 'ticket_id']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTickets
        fields = ['used', 'amount', 'id', 'client_id', 'event_id', 'ticket_id']
