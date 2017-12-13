"""
Django models
"""
from __future__ import unicode_literals

import os
import time
from datetime import date, datetime, time

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.timezone import make_aware

ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3


class Attachments(models.Model):
    """
    Attachment table in the database.
    """

    def get_file_path(self, filename):
        # pylint: disable=no-member
        folder = self.issue.title
        # pylint: enable=no-member
        return os.path.join('uploads', folder, filename)

    issue = models.ForeignKey('Issues', models.DO_NOTHING,
                              blank=True, null=True)
    image_url = models.ImageField(
        blank=True, null=True, upload_to=get_file_path)

    class Meta:
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
        app_label = 'city_issues'
        managed = False
        db_table = 'category'


class Statuses(models.Model):
    """
    Status table in the database.
    """
    status = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'city_issues'
        managed = False
        db_table = 'statuses'


class IssueHistory(models.Model):
    """
    IssueHistory table in the database.
    """
    STATUS_ID_NEW = Statuses.objects.get(id=1)

    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    issue = models.ForeignKey('Issues', models.DO_NOTHING,
                              blank=True, null=True)
    status = models.ForeignKey('Statuses', models.DO_NOTHING,
                               blank=True, null=True, default=STATUS_ID_NEW)
    transaction_date = models.DateTimeField(blank=True, null=True,
                                            auto_now_add=True)

    class Meta:
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
        app_label = 'city_issues'
        managed = False
        db_table = 'issues'

    def get_role_based_query(self, request):
        """Return issues based on role and author."""
        if request.user.is_anonymous():
            query = Issues.objects.filter(status__in=["open", "closed"])
        if request.user.is_authenticated() and request.user.role.id not in (ROLE_ADMIN, ROLE_MODERATOR):
            query = Issues.objects.filter(
                Q(status__in=["open", "closed"]) | Q(user=request.user.id)).exclude(status="deleted")
        if request.user.is_authenticated() and request.user.role.id in (ROLE_ADMIN, ROLE_MODERATOR):
            query = Issues.objects.all()
        return query

    def issue_filter(self, form, role_based_query):
        """Filter issue by form data."""
        kwargs = {}
        map_date_from = form.cleaned_data.get('date_from')
        map_date_to = form.cleaned_data.get('date_to')
        status_arr = form.data.get('status_arr').split(",")
        category = form.data.get('category')
        search = form.cleaned_data.get('search')

        if status_arr:
            kwargs["status__in"] = status_arr

        date_from = make_aware(datetime(1970, 1, 1,))
        date_to = make_aware(datetime.now())

        if map_date_from:
            date_from = make_aware(
                datetime.combine(map_date_from, time.min))
        if map_date_to:
            date_to = make_aware(datetime.combine(map_date_to, time.max))

        kwargs["open_date__range"] = (date_from, date_to)

        if category:
            kwargs['category'] = category

        query = role_based_query.filter(**kwargs)

        if search:
            query = role_based_query.filter(**kwargs).filter(
                Q(title__icontains=search) | Q(description__icontains=search))
        return query

    def get_issue_data_by_id(self, request, issue_id):
        """Get single issue data."""
        attachments_query = list(
            Attachments.objects.filter(issue=issue_id).values())

        comments_list = Comments()
        comments_query = comments_list.get_comments(issue_id)
        for comment in comments_query:
            comment['date_public'] = self.convert_date(comment['date_public'])

        images_urls = [item['image_url'] for item in attachments_query]
        checked_img_urls = []

        for img in images_urls:
            if img and os.path.isfile(os.path.join(settings.MEDIA_ROOT, img)):
                checked_img_urls.append(img)

        issue_obj = Issues.objects.filter(
            pk=issue_id).select_related("category")
        unpacked_issue_obj = issue_obj[0]

        issue_is_editable = False

        if hasattr(request.user, 'role') and (
                (request.user.role.id in (ROLE_ADMIN, ROLE_MODERATOR)) or
                (unpacked_issue_obj.user_id == request.user.id)):
            issue_is_editable = True

        issue_query = list(issue_obj.values(
            "title",
            "user",
            "category",
            "location_lat",
            "location_lon",
            "status",
            "description",
            "open_date",
            "close_date",
            "delete_date",
            "category__category",))

        issue_dict = issue_query[0]
        issue_dict['images_urls'] = checked_img_urls
        issue_dict['editable'] = issue_is_editable
        issue_dict['comments'] = comments_query

        issue_dict['open_date'] = self.convert_date(issue_dict['open_date'])
        issue_dict['close_date'] = self.convert_date(issue_dict['close_date'])
        issue_dict['delete_date'] = self.convert_date(
            issue_dict['delete_date'])

        return issue_query

    def convert_date(self, obj):
        """Converts data field from database to json acceptable format"""
        if isinstance(obj, (date, datetime)):
            return obj.isoformat(str(" "))
        return obj


class Comments(models.Model):
    """
    Issues table in the database.
    """
    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    issue = models.ForeignKey('Issues', models.DO_NOTHING)
    comment = models.TextField(max_length=400, null=False, blank=False)
    date_public = models.DateTimeField(auto_now_add=True)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'comments'

    def get_comments(self, issue_id):
        """Gets last three comments."""
        comments_query = list(
            Comments.objects.filter(issue=issue_id).select_related("user").order_by('date_public').values(
                "user__alias",
                "comment",
                "date_public",
            ))[::-1][:3]
        return comments_query
