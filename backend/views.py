# -*- coding: utf-8 -*-

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import template
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse, Http404

from backend.forms import SignUpForm
from backend.models import Event, TicketType, ClientTickets
from .permission import ReadOnly
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter

from serializers import ClientTickets, TicketSerializer, TicketListSerializer, EventListSerializer, EventSerializer
import backend.personal as pers
from operator import attrgetter

register = template.Library()


def event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return e404(request)
    ticket_types = TicketType.objects.filter(event_id=event_id)
    print(ticket_types)

    return render(request, 'backend/event.html', {'event': event, 'ticket_types': ticket_types})

def index(request):
    context = {}
    #search bar logic part
    query=""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    events = get_client_search(query)
    for event in events:
        if len(event.descriptions) >= 120:
            event.descriptions = event.descriptions[0:120] + "..."
    events = sorted(events, key=attrgetter('event_date'))
    context['all_events_info'] = [events[r * 3:(r + 1) * 3] for r in range(len(events))]
    print(context['all_events_info'])

    return render(request, 'backend/main.html', context)



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def my_logout(request):
    logout(request)
    response = redirect('/')
    return response


def e404(request):
    return render(request, 'backend/404.html')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        # data['add'] = self.user.add
        data['id'] = self.user.id
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class EventListAPI(generics.ListCreateAPIView):
    permission_classes = [] if pers.disableAuth else [IsAdminUser | ReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = [
        'id', 'event_name', 'descriptions', 'event_date', 'city', 'street', 'post_code', 'street_address', 'country']
    ordering_fields = ['id', 'event_name', 'event_date', 'city', 'country']


class EventDetailsAPI(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    permission_classes = [] if pers.disableAuth else [IsAdminUser | ReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'


class UserTicketListAPI(generics.ListAPIView):
    permission_classes = [] if pers.disableAuth else [IsAdminUser]
    queryset = ClientTickets.objects.all()
    serializer_class = TicketListSerializer


class TicketDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [] if pers.disableAuth else [IsAdminUser]
    queryset = ClientTickets.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'id'


@api_view(['GET', 'PATCH'])
@permission_classes((IsAdminUser,))
def validate_ticket(request, id):
    ticket = ClientTickets.objects.get(id=id)
    if ticket.used:
        return Response("ERROR: The ticket is already validated!", status=status.HTTP_403_FORBIDDEN)
    serializer = TicketSerializer(ticket, data={"used": True}, partial=True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    return Response("The ticket successfully validated.", status=status.HTTP_200_OK)
    # alternative: return Response(serializer.data, status=status.HTTP_200_OK)

def get_client_search(query=None):
    queryset = []
    queries = query.split(" ")
    print(queries)
    for word in queries:
        events = Event.objects.filter(
            Q(event_name__icontains=word) |
            Q(descriptions__icontains=word) |
            Q(city__icontains=word) |
            Q(country__icontains=word)
        ).distinct() #return uniq results

        for event in events:
            queryset.append(event)
    print(list(queryset))
    return list(set(queryset))

