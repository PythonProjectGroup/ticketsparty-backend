# -*- coding: utf-8 -*-
import json
from operator import attrgetter

from django import template
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime

import backend.errors
import backend.personal as pers
from backend.forms import SignUpForm
from backend.models import Event, TicketType
from serializers import ClientTickets, TicketSerializer, EventListSerializer, \
    EventSerializer, \
    EventKeySerializer
from .permission import ReadOnly

register = template.Library()


def event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return e404(request)

    ticket_types = []
    pictures = json.loads(event.pictures)
    if request.method == 'POST':
        print(request.POST)
        ticket_type_id = int(request.POST.get('ticket_type_id', -1))
        client_id = request.user.id
        name = request.POST.get('ticket_name', None)
        amount = request.POST.get('amount', 0)
        if not name or ticket_type_id == -1:
            print("Warning: Malformed post")
        else:
            try:
                ClientTickets(client_id_id=int(client_id),
                              event_id_id=int(event_id),
                              ticket_id_id=int(ticket_type_id),
                              amount=int(amount),
                              names=name).save()
            except backend.errors.NoAvailableTickets as e:
                return render(request, 'backend/errors/no_tickets.html',
                              {'amount': e.args[0]})
            except backend.errors.UserHasExceededTheTicketAmountLimit as e:
                return render(request,
                              'backend/errors/user_tickets_limit.html',
                              {'amount': e.args[0]})
    for ticket in TicketType.objects.filter(event_id=event_id):
        a = min(ticket.available_amount,
                ticket.max_per_client - ticket.calculate_amount_of_user_tickets(
                    client_id=request.user.id))
        b = [x for x in range(1, 1 + a)]
        ticket_types.append([b, ticket, a])
    return render(request, 'backend/event.html',
                  {'event': event, 'ticket_types': ticket_types,
                   'pictures': pictures})


def index(request):
    context = {}
    # search bar logic part
    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    events = get_client_search(query)
    for event in events:
        event.pictures = json.loads(event.pictures)[0]
        if len(event.descriptions) >= 120:
            event.descriptions = event.descriptions[0:120] + "..."
    events = sorted(events, key=attrgetter('event_date'))
    context['all_events_info'] = [events[x:x + 3] for x in
                                  range(0, len(events), 3)]
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


def tickets(request):
    tickets = ""
    if request.user.is_authenticated:
        tickets = ClientTickets.objects.filter(client_id=request.user)

    return render(request, 'backend/tickets.html', {'tickets': tickets})


def event_apikey(request, id):
    events = Event.objects.filter(id=id)
    return render(request, 'backend/event_apikey.html', {'events': events})


def e404(request):
    return render(request, '404.html')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        # data['add'] = self.user.add
        data['id'] = self.user.id
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class EventListAPI(generics.ListCreateAPIView):
    permission_classes = [] if pers.disableAuth else [ReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = [
        'id', 'event_name', 'descriptions', 'event_date', 'city', 'street',
        'post_code', 'street_address', 'country']
    ordering_fields = ['id', 'event_name', 'event_date', 'city', 'country']


class EventDetailsAPI(generics.RetrieveUpdateDestroyAPIView,
                      generics.CreateAPIView):
    permission_classes = [] if pers.disableAuth else [ReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'


class TicketDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [] if pers.disableAuth else []
    queryset = ClientTickets.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'ticket_hash'


class EventKeys(generics.ListAPIView):
    serializer_class = EventKeySerializer
    permission_classes = [] if pers.disableAuth else [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (user,)


@api_view(['GET', 'PATCH'])
@permission_classes(())
def validate_ticket(request, ticket_hash):
    try:
        ticket = ClientTickets.objects.filter(ticket_hash=ticket_hash)
        if ticket is not None:
            print(ticket)
            if ticket[0].used:
                return Response(serializers.serialize("json", ticket),
                                status=status.HTTP_403_FORBIDDEN)
            serializer = TicketSerializer(ticket[0], data={"used": True},
                                          partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializers.serialize("json", ticket),
                            status=status.HTTP_200_OK)
    except IndexError:
        return Response("Invalid ticket", status=status.HTTP_404_NOT_FOUND)
    # alternative: return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def manage_eventkey(request, slug):
    # [{"key":"abc123456", "event_id":6}, {...}]
    if request.method == 'POST':
        currentkeys = request.user.eventkeys
        if currentkeys:
            keyslist = json.loads(currentkeys)
        else:
            keyslist = []
        events = Event.objects.filter(eventkey=slug)
        if len(events) > 0:
            event_id = events[0].id
            for key in keyslist:
                if slug == key['key']:
                    return Response(status=status.HTTP_200_OK)
            else:
                keyslist.append({"key": slug, "event_id": event_id})
                print(keyslist)
                request.user.eventkeys = str(keyslist).replace('\'', '\"')
                request.user.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        currentkeys = request.user.eventkeys
        if currentkeys:
            keyslist = json.loads(currentkeys)
            keyindex = -1
            for index, key in enumerate(keyslist):
                if key['key'] == slug:
                    keyindex = index
            if keyindex != -1:
                keyslist.pop(keyindex)
                request.user.eventkeys = str(keyslist).replace('\'', '\"')
                request.user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
        ).distinct()  # return uniq results

        for event in events:
            queryset.append(event)
    print(list(queryset))
    return list(set(queryset))


# @api_view(['GET', 'PATCH'])
# @permission_classes((IsAdminUser,))
def add_event(request):
    try:
        if request.method == 'POST' and request.FILES['files']:
            uploaded_file_url = []
            fs = FileSystemStorage()
            invalid = []
            for f in request.FILES.getlist('files'):
                if (
                        f.content_type == 'image/jpeg' or f.content_type == 'image/png') and f.size < 5000001:
                    filename = fs.save(f.name, f)
                    uploaded_file_url.append(fs.url(filename))
                else:
                    invalid.append(f.name)
            organizer_name = request.POST.get('organizer_name', None)
            coordinates = request.POST.get('coordinates', None)
            event_name = request.POST.get('event_name', None)
            descriptions = request.POST.get('descriptions', None)
            city = request.POST.get('city', None)
            street = request.POST.get('street', None)
            post_code = request.POST.get('post_code', None)
            street_address = request.POST.get('street_address', None)
            country = request.POST.get('country', 'Poland')
            # Trzeba zrobić dobrze datę

            # event_date = time.strptime(request.POST.get('event_date', None), '%y/%m/%d')
            # event_date =datetime.strptime('09/19/18 13:55:26', '%m/%d/%y %H:%M:%S')
            event_date = request.POST.get('event_date', None)
            if len(uploaded_file_url) > 0:
                try:
                    Event(
                        organizer_name=organizer_name,
                        coordinates=coordinates,
                        event_name=event_name,
                        descriptions=descriptions,
                        city=city,
                        street=street,
                        post_code=post_code,
                        street_address=street_address,
                        country=country,
                        event_date=event_date,
                        pictures=json.dumps(uploaded_file_url)
                    ).save()
                except:
                    return render(request, 'backend/add_event.html', {
                        'info': 'Nie udało się stworzyć wydarzenia, błędne dane'
                    })
                if len(invalid) == 0:
                    return render(request, 'backend/add_event.html', {
                        'uploaded_file_url': uploaded_file_url,
                        'info': "Stworzyłeś event"
                    })
                else:
                    return render(request, 'backend/add_event.html', {
                        'uploaded_file_url': uploaded_file_url,
                        'info': 'Błędne pliki to: ' + str(invalid)
                    })
            else:
                return render(request, 'backend/add_event.html', {
                    'info': 'Nie udało się stworzyć wydarzenia, błędne wszystkie pliki'
                })
    except MultiValueDictKeyError:
        return render(request, 'backend/add_event.html', {
            'info': 'Nie udało się stworzyć wydarzenia, brak plików'
        })
    return render(request, 'backend/add_event.html')
