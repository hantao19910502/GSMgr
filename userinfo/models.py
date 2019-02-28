#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import crypt
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = datetime.now()

        if not email and not username:
            raise ValueError('The given email and username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.username = username
        user.set_password(password)
        user.ssh_google_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))
        user.google_scratch_code = "\n".join(
            ["".join([str(x) for x in [random.randrange(0, 9) for _ in range(8)]]) for _ in range(5)])
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50,
                                unique=True, verbose_name="UserName")
    # han_name = models.CharField(max_length=10, default="", blank=True, verbose_name="中文名")
    key = models.TextField(default="", blank=True, verbose_name="Public Key")
    hash_password = models.CharField(default="", blank=True,
                                     max_length=200, verbose_name="Hash Password")
    email = models.EmailField(default="", unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, verbose_name="手机号", blank=True, null=True)

    vpn_google_key = models.CharField(max_length=20, blank=True, null=True)
    ssh_google_key = models.CharField(max_length=20, blank=True, null=True)
    google_scratch_code = models.CharField(max_length=60, blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = "user"

    def has_perms(self, perm_list, obj=None):
        """
     Returns True if the user has each of the specified permissions. If
     object is passed, it checks if the user has all required perms for this
     object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def save(self, *args, **kwargs):
        if self.hash_password:
            hash = crypt.crypt(self.hash_password, "$6$" + self.username + "$")
            self.hash_password = hash
        return super(User, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return "/user/profile/%s" % self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username



class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username',)
