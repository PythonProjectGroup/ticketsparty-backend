# -*- coding: utf-8 -*-

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import template

from django.db import transaction

from backend.models import Event

register = template.Library()


def index(request):
    events = Event.objects.all()
    return render(request, 'backend/index.html', {'all_events_info': events})


def my_logout(request):
    logout(request)
    response = redirect('/')
    return response


def e404(request):
    return render(request, 'backend/404.html')
