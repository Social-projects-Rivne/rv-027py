"""
Django views
"""
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import TemplateView

from forms.forms import IssueForm
from models.issues import Category


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


def add_issue(request):
    form = IssueForm()
    categories = Category.objects.all()
    errors = []

    if request.POST:
        request.POST.get('latitude')

    return render(request, 'issues/issues.html', {'form': form, 'categories': categories, 'errors': errors})
