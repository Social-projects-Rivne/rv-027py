"""
Django views
"""
# -*- coding: utf-8 -*-
import json
from datetime import date, datetime, time

from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views.generic import ListView


from city_issues.models import Attachments, Issues
from city_issues.forms.forms import EditIssue, IssueFilter, IssueForm


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


class IssueCreate(CreateView):
    model = Issues
    form_class = IssueForm
    template_name = 'issues/issues.html'
    success_url = 'add-issue'

    def form_valid(self, form):
        issue = form.save(commit=True)

        if form.files:
            self.save_file(form, form.files.getlist('file'), issue)

        messages.success(self.request, 'Issue was successfully saved')
        return super(IssueCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(IssueCreate, self).form_invalid(form)

    def save_file(self, form, files, issue):
        for file in files:
            if file._size > 5242880:
                messages.error(self.request, 'Max file size : 5MB')
                return super(IssueCreate, self).form_valid(form)
            else:
                attachment = Attachments()
                attachment.issue = issue
                attachment.image_url = file
                attachment.save()


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
    """Returns all issues records as json"""
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')

    if date_from_str or date_to_str:
        date_from = make_aware(datetime.combine(
            datetime.strptime(date_from_str, '%Y-%m-%d'), time.min))
        date_to = make_aware(datetime.combine(
            datetime.strptime(date_to_str, '%Y-%m-%d'), time.max))

        date_query = Issues.objects.filter(
            open_date__range=(date_from, date_to))
        data = serializers.serialize("json", date_query)
        return JsonResponse(data, safe=False)

    data = serializers.serialize("json", Issues.objects.all())
    return JsonResponse(data, safe=False)


def convert_date(obj):
    """Converts data field from database to json acceptable format"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


class CheckIssues(ListView):
    """A list of issues"""
    template_name = 'issues_list.html'
    model = Issues
    context_object_name = 'issues_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(CheckIssues, self).get_context_data(**kwargs)
        context['issues_range'] = range(context["paginator"].num_pages)
        return context
