# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
import json
from django import template


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(verbose_name="nazwa", blank=True, max_length=128, help_text="Imię i nazwisko pracownika")
    last_ip = models.CharField(null=True, verbose_name="last_login", blank=True, max_length=64,
                               help_text="Ostatnie ip z którego pracownik się logował")
    phone = models.CharField(blank=True, verbose_name="telefon", max_length=32, help_text="telefon do pracownika")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']


    def __str__(self):
        return str(self.name)

