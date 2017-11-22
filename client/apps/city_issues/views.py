"""
Django views
"""
# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages

from forms.forms import IssueForm
from models.issues import Attachments, Issues

from city_issues.models import Issues


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

        file = form.cleaned_data['file']
        if file:
            self.save_file(form, file, issue)

        messages.success(self.request, 'Issue was successfully saved')
        return super(IssueCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to save')
        return super(IssueCreate, self).form_invalid(form)

    def save_file(self, form, file, issue):
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
    return render(request, 'map_page.html')


def get_issue_data(request, issue_id):
    data = serializers.serialize("json", Issues.objects.filter(pk=issue_id))
    return JsonResponse(data, safe=False)


def get_all_issues_data(request):
    data = serializers.serialize("json", Issues.objects.all())
    return JsonResponse(data, safe=False)
