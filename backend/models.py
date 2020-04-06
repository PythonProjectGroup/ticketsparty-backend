# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
import json
from django import template



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, isAdmin,  **extra_fields, ):
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


class Client(models.Model):
    keeper = models.ForeignKey(get_user_model(), verbose_name="Opiekun", on_delete=models.CASCADE,
                               related_name='opiekun_klienta')
    name = models.CharField(verbose_name="nazwa", blank=True, max_length=128, help_text="Nazwa firmy lub imię i nazwisko")
    is_company = models.BooleanField(verbose_name="czy jest to firma", help_text="Zaznacz jeśli jest to firma (odznacz jeśli osoba prywatna)")
    street = models.CharField(blank=True, max_length=64, verbose_name="ulica", help_text="Podaj nazwę ulicy")
    home_number = models.CharField(blank=True, max_length=32, verbose_name="nr domu", help_text="Podaj numer domu i mieszkania")
    city = models.CharField(blank=True, max_length=32, verbose_name="miasto", help_text="Miasto z którego klient pochodzi")
    country = models.CharField(blank=True, max_length=32, verbose_name="kraj", help_text="Kraj z którego klient pochodzi")
    nip = models.CharField(blank=True, max_length=64, verbose_name="nip", help_text="Podaj nip firmy (puste jeśli nie dotyczy)")
    regon = models.CharField(blank=True, max_length=64, verbose_name="regon", help_text="Podaj regon firmy (puste jeśli nie dotyczy)")
    phone = models.CharField(blank=True, verbose_name="telefon", max_length=32, help_text="Podaj główny numer klienta")
    email = models.CharField(blank=True, verbose_name="email", max_length=128, help_text="Podaj główny e-mail klienta")
    description = models.TextField(verbose_name="opis", blank=True, help_text="Krótka notka na temat klienta")
    notes = models.TextField(verbose_name="komentarze", blank=True, help_text="Komentarze dotyczące klienta")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

class Product(models.Model):
    name = models.CharField(verbose_name="nazwa", blank=True, max_length=128, help_text="Imię i nazwisko osoby kontaktowej")
    description = models.TextField(verbose_name="description", help_text="Opis produktu")
    notes = models.TextField(verbose_name="komentarze", blank=True, help_text="Komentarze dotyczące produktu")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Produkty"
        verbose_name_plural = "Produkty"


class Entry(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produkt",  on_delete=models.CASCADE, related_name='opiekun_inwestycji')
    amount = models.IntegerField(verbose_name="ilosc", help_text="ilosc produktu (szt)")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="cena", help_text="Cena za maseczki (ogółem)")

    class Meta:
        verbose_name = "Wpis"
        verbose_name_plural = "Wpisy"

        def __str__(self):
            return str(self.amount)


class Order(models.Model):
    keeper = models.ForeignKey(get_user_model(), verbose_name="Opiekun",  on_delete=models.CASCADE, related_name='opiekun_zamowienia')
    company = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Klient")
    items = models.ManyToManyField(Entry)
    description = models.TextField(verbose_name="opis", help_text="krótki opis inwestycji")
    notes = models.TextField(verbose_name="komentarze", help_text="komentarze dotyczące inwestycji")


    def __str__(self):
        return str(self.company.name)

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

