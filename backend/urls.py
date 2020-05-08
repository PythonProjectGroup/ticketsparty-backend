# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'backend'  # przestrzeń nazw aplikacji
urlpatterns = [
    path('events/', views.event_list),
    path('events/<int:event_id>/', views.event_details),
    # path('tickets/', views.client_ticket_list),
    # path('tickets/<int:event_id>', views.ticket_details),
    path('tickets/<int:id>/check/', views.check_ticket),
    # path('tickets/<int:id>/validate/', views.validate_ticket),
]
