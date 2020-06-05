# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.dateparse import parse_date

from backend.errors import NoAvailableTickets, \
    UserHasExceededTheTicketAmountLimit, InvalidAmount, \
    PurchaseNotAvailableInThisPeriod, InvalidDate, InvalidData


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, isAdmin, **extra_fields):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, True, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(verbose_name="nazwa", blank=True, max_length=128,
                            help_text="Imię i nazwisko pracownika")
    phone = models.CharField(blank=True, verbose_name="telefon", max_length=32,
                             help_text="telefon do pracownika")
    eventkeys = models.TextField(verbose_name="klucze API", blank=True,
                                 default="[]")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = UserManager()

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    id = models.AutoField(primary_key=True),
    organizer_name = models.TextField(verbose_name="nazwa organizatora")
    coordinates = models.CharField(max_length=50,
                                   verbose_name="koordynaty wydarzenia",
                                   blank=True)
    event_name = models.CharField(max_length=80, verbose_name="nazwa eventu")
    descriptions = models.TextField(max_length=800, verbose_name="Opisy")
    pictures = models.TextField(max_length=800, verbose_name="Zdjęcia")
    event_date = models.DateTimeField(verbose_name="Data")
    timestamp = models.TextField(verbose_name="timestamp", blank=True)
    eventkey = models.TextField(verbose_name='event key', blank=True)
    city = models.CharField(max_length=50, verbose_name="Miasto")
    street = models.CharField(max_length=100, verbose_name="Ulica")
    post_code = models.CharField(max_length=10, verbose_name="Kod pocztowy")
    street_address = models.CharField(max_length=4,
                                      verbose_name="Numer adresu")
    country = models.CharField(max_length=20, verbose_name="Państwo")
    status = models.CharField(max_length=8, choices=[(tag, tag) for tag in
                                                     ['pending', 'rejected',
                                                      'accepted']],
                              default='pending')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        cur_time = str(time.time())
        if self.timestamp is None or self.timestamp == "":
            self.timestamp = cur_time
            self.eventkey = hashlib.sha256(
                str(cur_time).encode('utf-8')).hexdigest()
        else:
            if self.eventkey is None or self.eventkey == "":
                self.eventkey = hashlib.sha256(
                    str(self.timestamp).encode('utf-8')).hexdigest()

        super(Event, self).save(force_insert=force_insert,
                                force_update=force_update, using=using,
                                update_fields=update_fields)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"


class TicketType(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_name = models.CharField(max_length=150, verbose_name="Nazwa biletu")
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE,
                                 verbose_name="ID wydarzenia")
    start_of_selling = models.DateTimeField(verbose_name="Początek sprzedaży")
    end_of_selling = models.DateTimeField(verbose_name="Koniec sprzedaży")
    price = models.FloatField(verbose_name="Koszt biletu")
    available_amount = models.IntegerField(default=0,
                                           verbose_name="Dostępna ilość biletów")
    max_per_client = models.IntegerField(default=2,
                                         verbose_name="Ograniczenie na jednego klienta")

    def save(self, *args, **kwargs):
        start = timezone.make_aware(datetime.strptime(self.start_of_selling,'%Y-%m-%dT%H:%M'), timezone.utc)
        end = timezone.make_aware(datetime.strptime(self.end_of_selling,'%Y-%m-%dT%H:%M'), timezone.utc)
        if start > end or end > self.event_id.event_date:
            raise InvalidDate()
        if self.max_per_client < 1 or self.price < 0.0 or self.available_amount < 0.0:
            raise InvalidData()
        super(TicketType, self).save(args, kwargs)

    class Meta:
        verbose_name = "Rodzaj biletu"
        verbose_name_plural = "Rodzaje biletów"

    def calculate_amount_of_user_tickets(self, client_id):
        counter = 0
        for ticket in ClientTickets.objects.filter(client_id_id=client_id,
                                                   ticket_id__id=self.id):
            counter += ticket.amount
        return counter


class ClientTickets(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                  verbose_name="ID klienta")
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE,
                                 verbose_name="ID eventu")
    ticket_id = models.ForeignKey(TicketType, on_delete=models.CASCADE,
                                  verbose_name="ID rodzaju ticketu")
    timestamp = models.TextField(verbose_name="timestamp", blank=True)
    ticket_hash = models.TextField(verbose_name="ticket_hash", blank=True)
    bought_date = models.DateTimeField(verbose_name="Data zakupu",
                                       auto_now_add=True)
    amount = models.IntegerField(verbose_name="Ilość biletów")
    used = models.BooleanField(default=False, verbose_name="Wykorzystany")
    names = models.TextField(verbose_name="Zakupiony dla")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        cur_time = str(time.time())
        if self.timestamp is None or self.timestamp == "":
            self.timestamp = str(cur_time)

        if self.ticket_hash is None or self.ticket_hash == "":
            ticket_type = self.ticket_id
            if self.amount < 1:
                raise InvalidAmount(str(self.amount))
            if self.amount > ticket_type.available_amount:
                raise NoAvailableTickets(str(ticket_type.available_amount))
            if not (ticket_type.start_of_selling <= timezone.now()
                    < ticket_type.end_of_selling):
                raise PurchaseNotAvailableInThisPeriod()
            a = ticket_type.calculate_amount_of_user_tickets(self.client_id_id)
            if a + self.amount > ticket_type.max_per_client:
                raise UserHasExceededTheTicketAmountLimit(
                    str(ticket_type.max_per_client - a))
            else:
                ticket_type.available_amount -= self.amount
                ticket_type.save(update_fields=["available_amount"])
                if self.timestamp is None or self.timestamp == "":
                    self.ticket_hash = hashlib.sha256(
                        (str(cur_time) + str(self.client_id) + str(
                            self.client_id.email) + str(self.event_id)).encode(
                            'utf-8')).hexdigest()
                else:
                    self.ticket_hash = hashlib.sha256(
                        (str(self.timestamp) + str(self.client_id) + str(
                            self.client_id.email) + str(self.event_id)).encode(
                            'utf-8')).hexdigest()
        super(ClientTickets, self).save(force_insert=force_insert,
                                        force_update=force_update, using=using,
                                        update_fields=update_fields)

    class Meta:
        verbose_name = "Bilet klienta"
        verbose_name_plural = "Bilety klientów"
