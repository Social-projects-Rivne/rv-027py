from __future__ import unicode_literals

from django.db import models


class Roles(models.Model):
    role = models.TextField()

    class Meta:
        managed = False
        db_table = 'roles'


class Users(models.Model):
    name = models.TextField(blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    hashed_password = models.TextField(blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING, blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
