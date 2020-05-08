# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'backend'  # przestrzeń nazw aplikacji
urlpatterns = [
    url('events/', views.event_list),
    url('events/<int:event_id>/', views.event_details),
    # url('tickets/', views.client_ticket_list),
    # url('tickets/<int:event_id>', views.ticket_details),
    url('tickets/<int:id>/check/', views.check_ticket),
    # url('tickets/<int:id>/validate/', views.validate_ticket),
]
