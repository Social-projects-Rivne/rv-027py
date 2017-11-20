"""
Django views
"""
# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages

from forms.forms import AttachmentForm, IssueForm
from models.issues import Issues


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


class IssueCreate(CreateView):
    model = Issues
    form_class = IssueForm
    second_form_class = AttachmentForm
    template_name = 'issues/issues.html'
    success_url = 'add-issue'

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'Issue was successfully saved')
        return super(CreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to save')
        return super(CreateView, self).form_valid(form)
