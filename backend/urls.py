# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'backend'  # przestrzeń nazw aplikacji
urlpatterns = [
    path('events/', views.EventListAPI.as_view()),
    path('events/<int:id>/', views.EventDetailsAPI.as_view()),
    path('tickets/', views.UserTicketListAPI.as_view()),
    path('tickets/<int:id>/', views.TicketDetailsAPI.as_view()),
    path('tickets/<int:id>/validate/', views.validate_ticket),
]
