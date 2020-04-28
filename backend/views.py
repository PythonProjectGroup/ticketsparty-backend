# -*- coding: utf-8 -*-

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import template
from django.db import transaction
from django.contrib.auth import get_user_model

from backend.forms import SignUpForm
from backend.models import Event
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

register = template.Library()


def index(request):
    events = Event.objects.all()
    for event in events:
        if len(event.descriptions) >= 120:
            event.descriptions = event.descriptions[0:120]+"..."
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
        #data['add'] = self.user.add
        data['id'] = self.user.id
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
