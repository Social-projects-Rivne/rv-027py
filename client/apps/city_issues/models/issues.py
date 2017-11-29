"""
Django models
"""
from __future__ import unicode_literals

import os
import time
from django.db import models


class Attachments(models.Model):
    """
    Attachment table in the database.
    """

    def get_file_path(self, filename):
        folder = self.issue.title
        return os.path.join('uploads', folder, filename)

    issue = models.ForeignKey('Issues', models.DO_NOTHING,
                              blank=True, null=True)
    image_url = models.ImageField(blank=True, null=True, upload_to=get_file_path)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'attachments'


class Category(models.Model):
    """
    Category table in the database.
    """
    category = models.TextField(blank=True, null=True)
    favicon = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.category)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'category'


class IssueHistory(models.Model):
    """
    IssueHistory table in the database.
    """
    STATUS_ID_NEW = 1

    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    issue = models.ForeignKey('Issues', models.DO_NOTHING,
                              blank=True, null=True)
    status = models.ForeignKey('Statuses', models.DO_NOTHING,
                               blank=True, null=True, default=STATUS_ID_NEW)
    transaction_date = models.DateTimeField(blank=True, null=True,
                                            auto_now_add=True)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'issue_History'


class Issues(models.Model):
    """
    Issues table in the database.
    """
    title = models.TextField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    category = models.ForeignKey('Category', models.DO_NOTHING)
    location_lat = models.FloatField(blank=True, null=True)
    location_lon = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True, default='new')
    description = models.TextField(blank=True, null=True)
    open_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    close_date = models.DateTimeField(blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'issues'


class Statuses(models.Model):
    """
    Status table in the database.
    """
    status = models.TextField(blank=True, null=True)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'statuses'
