# -*- coding: utf-8 -*-

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import template
from django.db import transaction
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.forms import SignUpForm
from backend.models import Event, TicketType, ClientTickets
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from serializers import ClientTickets, TicketSerializer, TicketListSerializer, EventListSerializer, EventSerializer

register = template.Library()


def event(request, event_id):
    event = Event.objects.get(id=event_id)
    ticket_types = TicketType.objects.filter(event_id=event_id)
    print(ticket_types)
    return render(request, 'backend/event.html', {'event': event, 'ticket_types': ticket_types})


def index(request):
    events = Event.objects.all()
    for event in events:
        if len(event.descriptions) >= 120:
            event.descriptions = event.descriptions[0:120] + "..."
    events_in_rows = [events[r * 3:(r + 1) * 3] for r in range(len(events))]
    print(events_in_rows)
    return render(request, 'backend/index.html', {'all_events_info': events_in_rows})


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


@csrf_exempt
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventListSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventListSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return JsonResponse(serializer.data)

# @csrf_exempt
# def client_ticket_list(request):
#     if request.method == 'GET':
#         tickets = ClientTickets.objects.all()
#         serializer = TicketListSerializer(tickets, many=True)
#         return JsonResponse(serializer.data, safe=False)

# @csrf_exempt
# def ticket_details(request, event_id):
#     try:
#         ticket = ClientTickets.objects.get(id=event_id)
#     except ClientTickets.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = TicketSerializer(ticket)
#         return JsonResponse(serializer.data)

@csrf_exempt
def check_ticket(request, id):
    try:
        ticket = ClientTickets.objects.get(id=id)
    except TicketType.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TicketSerializer(ticket)
        return JsonResponse(serializer.data)

# @csrf_exempt
# def validate_ticket(request, id):
#     try:
#         ticket = ClientTickets.objects.get(id=id)
#     except TicketType.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'PUT':
#         ticket.used = True
#         ticket.save()
#         return HttpResponse(status=200)
