from __future__ import unicode_literals

from django.db import models


class Attachments(models.Model):
    issue = models.ForeignKey('Issues', models.DO_NOTHING, blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attachments'


class Category(models.Model):
    category = models.TextField(blank=True, null=True)
    favicon = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class IssueHistory(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    issue = models.ForeignKey('Issues', models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('Statuses', models.DO_NOTHING, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue_History'


class Issues(models.Model):
    name = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issues'


class Statuses(models.Model):
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statuses'
