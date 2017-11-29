"""
Django views
"""
# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from city_issues.models import Attachments, Issues, IssueHistory, User
from city_issues.forms.forms import EditIssue, IssueForm


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


class UserProfileView(View):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_issues = IssueHistory.objects.filter(user=user).select_related('issue')

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
    return render(request, 'map_page.html')


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
    data = serializers.serialize(
        "json", Issues.objects.filter(pk=issue_id).select_related())
    return JsonResponse(data, safe=False)


def get_all_issues_data(request):
    """Returns all issues records as json"""
    data = serializers.serialize("json", Issues.objects.all())
    return JsonResponse(data, safe=False)
