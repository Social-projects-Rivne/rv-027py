"""
Django views
"""
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import FormView, CreateView
from django.views.generic.base import TemplateView, View

from forms.forms import IssueForm
from models.issues import Issues


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


class IssueCreate(CreateView):
    model = Issues
    form_class = IssueForm
    template_name = 'issues/issues.html'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponse("Saved")
