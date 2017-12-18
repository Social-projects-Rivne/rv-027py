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

    def delete(self, *args, **kwargs):
        # pylint: disable=no-member
        storage, path = self.image_url.storage, self.image_url.path
        # pylint: enable=no-member
        super(Attachments, self).delete(*args, **kwargs)
        directory_path = os.path.abspath(os.path.join(path, os.pardir))

        storage.delete(path)
        if not os.listdir(directory_path):
            os.rmdir(directory_path)

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

    def __unicode__(self):
        return u'{0}'.format(self.status)

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

    def get_attachments(self):
        return Attachments.objects.filter(issue=self.id)

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
        dict_of_actions = self.get_actions_list(request, issue_id)

        attachments_query = list(
            Attachments.objects.filter(issue=issue_id).values())

        comments_list = Comments()
        comments_query = comments_list.get_comments(
            issue_id, dict_of_actions['list_of_comments_statuses'])

        images_urls = [item['image_url'] for item in attachments_query]
        checked_img_urls = []

        for img in images_urls:
            if img and os.path.isfile(os.path.join(settings.MEDIA_ROOT, img)):
                checked_img_urls.append(img)

        issue_obj = Issues.objects.filter(
            pk=issue_id).select_related("category")
        unpacked_issue_obj = issue_obj[0]

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
        issue_dict['dict_of_actions'] = dict_of_actions
        issue_dict['comments'] = comments_query

        issue_dict['open_date'] = convert_date(issue_dict['open_date'])
        issue_dict['close_date'] = convert_date(issue_dict['close_date'])
        issue_dict['delete_date'] = convert_date(
            issue_dict['delete_date'])

        return issue_query

    def get_actions_list(self, request, issue_id):
        """Return list of allowed actions with issue."""
        list_of_comments_statuses = ['public']
        list_of_actions = []

        if request.user.is_authenticated():

            issue = Issues.objects.get(pk=issue_id)

            user_is_admin_or_moderator = request.user.role.id in (
                ROLE_ADMIN, ROLE_MODERATOR)

            user_is_issue_owner = (issue.user_id == request.user.id)

            if user_is_admin_or_moderator:
                list_of_actions.append('edit')
                list_of_comments_statuses.append('private')
                list_of_comments_statuses.append('internal')

                if issue.status in ('new', 'on moderation'):
                    list_of_actions.append("open")

                if issue.status in ('open', 'pending close'):
                    list_of_actions.append("closed")

                if issue.status != 'deleted':
                    list_of_actions.append("deleted")
            else:
                if user_is_issue_owner:
                    list_of_comments_statuses.append('private')

                    if issue.status in ('new', 'on moderation'):
                        list_of_actions.append("edit")
                    if issue.status == 'open':
                        list_of_actions.append("pending close")

        dict_of_actions = {
            'list_of_comments_statuses': list_of_comments_statuses,
            'list_of_actions': list_of_actions
        }

        return dict_of_actions


class Comments(models.Model):
    """
    Issues table in the database.
    """
    user = models.ForeignKey('User', models.DO_NOTHING,
                             blank=True, null=True)
    issue = models.ForeignKey('Issues', models.DO_NOTHING)
    comment = models.TextField(max_length=400, null=False, blank=False)
    date_public = models.DateTimeField(auto_now_add=True)
    status = models.TextField(null=False)

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'comments'

    def get_comments(self, issue_id, allowed_statuses_to_return):
        """Gets last three comments."""
        kwargs = {
            'issue': issue_id,
            'status__in': allowed_statuses_to_return,
        }
        comments_query = list(
            Comments.objects.filter(**kwargs).select_related("user").order_by('date_public').values(
                "user__alias",
                "comment",
                "date_public",
                "status",
            )[::-1])

        for comment in comments_query:
            comment['date_public'] = convert_date(comment['date_public'])

        return comments_query


def convert_date(obj):
    """Converts data field from database to json acceptable format"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat(str(" "))
    return obj
