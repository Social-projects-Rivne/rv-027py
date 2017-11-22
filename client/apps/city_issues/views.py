"""
Django views
"""
# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages

from forms.forms import IssueForm
from models.issues import Attachments, Issues


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

        if self.validate_file(file):
            attachment = Attachments()
            attachment.issue = issue
            attachment.image_url = file
            attachment.save()
            messages.success(self.request, 'Issue was successfully saved')

        return super(IssueCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to save')
        return super(IssueCreate, self).form_invalid(form)

    def validate_file(self, file):
        if file._size > 5242880:
            messages.error(self.request, 'Max file size : 5MB')
        else:
            return True


