# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
import json


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50, verbose_name="nazwa eventu")
    descriptions = models.TextField(max_length=800, verbose_name="Opisy")
    pictures = models.TextField(max_length=800, verbose_name="Zdjęcia")
    event_date = models.DateTimeField(verbose_name="Data")
    city = models.CharField(max_length=20, verbose_name="Miasto")
    street = models.CharField(max_length=30, verbose_name="Ulica")
    post_code = models.CharField(max_length=6, verbose_name="Kod pocztowy")
    street_address = models.CharField(max_length=4, verbose_name="Numer adresu")
    country = models.CharField(max_length=20, verbose_name="Państwo")

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"


class TicketType(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="ID wydarzenia")
    start_of_selling = models.DateTimeField(verbose_name="Początek sprzedaży")
    end_of_selling = models.DateTimeField(verbose_name="Koniec sprzedaży")
    price = models.FloatField(verbose_name="Koszt biletu")
    available_amount = models.IntegerField(default=0, verbose_name="Dostępna ilość biletów")
    max_per_client = models.IntegerField(default=2, verbose_name="Ograniczenie na jednego klienta")

    class Meta:
        verbose_name = "Rodzaj biletu"
        verbose_name_plural = "Rodzaje biletów"


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="Nazwisko")
    surname = models.CharField(max_length=20, verbose_name="Imię")
    email = models.EmailField(verbose_name="Adres mailowy")
    password = models.CharField(max_length=25, verbose_name="Hasło")

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"


class ClientTickets(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="ID klienta")
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="ID eventu")
    ticket_id = models.ForeignKey(TicketType, on_delete=models.CASCADE, verbose_name="ID rodzaju ticketu")
    bought_date = models.DateTimeField(verbose_name="Data zakupu")
    amount = models.IntegerField(verbose_name="Ilość biletów")
    used = models.BooleanField(default=False, verbose_name="Wykorzystany")
    names = models.TextField(verbose_name="Zakupiony dla")

    def save(self, *args, **kwargs):
        self.names = json.dumps(self.names)
        super(ClientTickets, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Bilet klienta"
        verbose_name_plural = "Bilety klientów"


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, isAdmin, **extra_fields, ):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if isAdmin:
            pass
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

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
    name = models.CharField(verbose_name="nazwa", blank=True, max_length=128, help_text="Imię i nazwisko pracownika")
    last_ip = models.CharField(null=True, verbose_name="last_login", blank=True, max_length=64,
                               help_text="Ostatnie ip z którego pracownik się logował")
    phone = models.CharField(blank=True, verbose_name="telefon", max_length=32, help_text="telefon do pracownika")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = UserManager()

    def __str__(self):
        return str(self.name)
