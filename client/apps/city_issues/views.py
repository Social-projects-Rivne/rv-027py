"""
Django views
"""
# -*- coding: utf-8 -*-
import json
from datetime import date, datetime, time
import operator

from django.db.models import Q
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views.generic import CreateView, FormView, ListView

from city_issues.models import Attachments, Issues,  IssueHistory, User
from city_issues.forms.forms import EditIssue, IssueFilter, IssueForm, IssueSearchForm


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


class UserProfileView(View):
    """User profile page"""
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_issues = Issues.objects.filter(user_id=user_id)

        return render(request, 'user/user.html', {'user': user, 'user_issues': user_issues})


class IssueCreate(CreateView):
    """Create new issue"""
    MAX_FILE_SIZE = 5242880

    model = Issues
    form_class = IssueForm
    template_name = 'issues/issues.html'
    success_url = 'add-issue'

    def form_valid(self, form):
        form.instance.user = self.request.user
        issue = form.save(commit=True)

        if form.files:
            self.save_files(form, form.files.getlist('files'), issue)

        self.save_issue_history(issue, form.instance.user)
        messages.success(self.request, 'Issue was successfully saved')
        return super(IssueCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(IssueCreate, self).form_invalid(form)

    def save_files(self, form, files, issue):
        for issue_file in files:
            if issue_file._size > self.MAX_FILE_SIZE:
                messages.error(self.request, 'Max file size : 5MB')
                return super(IssueCreate, self).form_valid(form)
            else:
                attachment = Attachments()
                attachment.issue = issue
                attachment.image_url = issue_file
                attachment.save()

    def save_issue_history(self, issue, user):
        issue_history = IssueHistory()
        issue_history.issue = issue
        issue_history.user = user
        issue_history.save()


def map_page_view(request):
    """Map page"""
    form = IssueFilter()
    return render(request, 'map_page.html', {'form': form})


def edit_issue_view(request, issue_id):
    """Edit page"""
    if request.method == 'POST':
        form = EditIssue(request.POST)
        if form.is_valid():
            EditIssue(request.POST, instance=Issues.objects.get(
                pk=issue_id)).save()
            return redirect(reverse('map'))
    else:
        form = EditIssue(instance=Issues.objects.get(pk=issue_id))

    return render(
        request, 'edit_issue.html', {'form': form, 'issue_id': issue_id})


def get_issue_data(request, issue_id):
    """Returns single issue record as json"""

    attachments_query = list(
        Attachments.objects.filter(issue=issue_id).values())
    images_urls = [item['image_url'] for item in attachments_query]

    issue_query = list(Issues.objects.filter(pk=issue_id).values())
    issue_dict = issue_query[0]
    issue_dict['images_urls'] = images_urls

    issue_dict['open_date'] = convert_date(issue_dict['open_date'])
    issue_dict['close_date'] = convert_date(issue_dict['close_date'])
    issue_dict['delete_date'] = convert_date(issue_dict['delete_date'])

    data = json.dumps(issue_query)
    return JsonResponse(data, safe=False)


def get_all_issues_data(request):
    """Returns all issues records as json with possible filter."""
    data = serializers.serialize(
        "json",
        Issues.objects.filter(close_date__isnull=True))

    form = IssueFilter(request.GET)

    if form.is_valid() and form.data.get('filter'):

        map_date_from = form.data.get('date_from')
        map_date_to = form.data.get('date_to')
        show_closed = form.data.get('show_closed')
        category = form.data.get('category')
        search = form.data.get('search')

        if show_closed == 'true':
            show_closed = False
        else:
            show_closed = True

        kwargs = {"close_date__isnull": (show_closed)}

        if map_date_from and map_date_to:
            date_from = make_aware(datetime.combine(
                datetime.strptime(map_date_from, '%Y-%m-%d'), time.min))
            date_to = make_aware(datetime.combine(
                datetime.strptime(map_date_to, '%Y-%m-%d'), time.max))
            kwargs["open_date__range"] = (date_from, date_to)

        if category:
            kwargs['category'] = category

        query = Issues.objects.filter(**kwargs)

        if search:
            query = Issues.objects.filter(**kwargs).filter(
                Q(title__icontains=search) | Q(description__icontains=search))

        data = serializers.serialize("json", query)

    return JsonResponse(data, safe=False)


def convert_date(obj):
    """Converts data field from database to json acceptable format"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


class CheckIssues(ListView, FormView):
    """A list of issues"""
    form_class = IssueSearchForm
    template_name = 'issues_list.html'
    model = Issues
    context_object_name = 'issues_list'
    paginate_by = 6

    # def search_issue(self):
    #     search = self.request.GET.get('search')
    #     all_issue = Issues.objects.all()
    #     if search:
    #         query_list = search.split()
    #         issues_list = all_issue.filter(
    #             reduce(operator.or_, (Q(title__icontains=q) for q in query_list)) |
    #             reduce(operator.or_, (Q(description__icontains=q) for q in query_list)))
    #         return issues_list

    def get_queryset(self):
        """Adds sorting"""
        queryset = super(CheckIssues, self).get_queryset()
        order_by = self.request.GET.get('order_by', 'title')
        search = self.request.GET.get('search')
        if search:
            query_list = search.split()
            queryset = queryset.filter(
                reduce(operator.or_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.or_, (Q(description__icontains=q) for q in query_list))
            )
        if order_by in ('title', 'status', 'description', 'category'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == 'v_v':
                queryset = queryset.reverse()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CheckIssues, self).get_context_data(**kwargs)
        context['issues_range'] = range(context["paginator"].num_pages)
        return context

def search_issue(request):
    """ Search issues """
    form = IssueSearchForm
    search = request.GET.get('search')
    all_issue = Issues.objects.all()
    if search:
        query_list = search.split()
        issues_list = all_issue.filter(
            reduce(operator.or_, (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.or_, (Q(description__icontains=q) for q in query_list)))
    return render (request, 'issues_list.html',  {'form': form, 'issues_list': issues_list})