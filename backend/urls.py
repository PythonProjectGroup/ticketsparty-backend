# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = 'backend'  # przestrzeń nazw aplikacji
urlpatterns = [
    path('events/', views.EventListAPI.as_view()),
    path('events/<int:id>/', views.EventDetailsAPI.as_view()),
    path('eventkeys/', views.EventKeys.as_view()),
    path('eventkeys/<slug:slug>', views.manage_eventkey),
    path('tickets/<str:ticket_hash>/validate/', views.validate_ticket),
    path('tickets/<str:ticket_hash>', views.TicketDetailsAPI.as_view(), name='ticket'),
    path('tickets/', views.tickets),
]
