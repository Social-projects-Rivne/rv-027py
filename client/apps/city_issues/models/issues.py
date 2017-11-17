"""
Django models
"""
from __future__ import unicode_literals

from django.db import models


class Attachments(models.Model):
    """
    Attachment table in the database.
    """
    issue = models.ForeignKey('Issues', models.DO_NOTHING,
                              blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        """..."""
        managed = False
        db_table = 'attachments'


class Category(models.Model):
    """
    Category table in the database.
    """
    category = models.TextField(blank=True, null=True)
    favicon = models.TextField(blank=True, null=True)

    class Meta:
        """..."""
        managed = False
        db_table = 'category'


class IssueHistory(models.Model):
    """
    IssueHistory table in the database.
    """
    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    issue = models.ForeignKey('Issues', models.DO_NOTHING,
                              blank=True, null=True)
    status = models.ForeignKey('Statuses', models.DO_NOTHING,
                               blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True,
                                            null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        """..."""
        managed = False
        db_table = 'issue_History'


class Issues(models.Model):
    """
    Issues table in the database.
    """
    name = models.TextField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        """..."""
        managed = False
        db_table = 'issues'


class Statuses(models.Model):
    """
    Status table in the database.
    """
    status = models.TextField(blank=True, null=True)

    class Meta:
        """..."""
        managed = False
        db_table = 'statuses'
