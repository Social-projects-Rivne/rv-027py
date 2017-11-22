"""
Django views
"""
# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.urls import reverse

from city_issues.models import Issues, Category
from forms.forms import EditIssue


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


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
