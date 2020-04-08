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
