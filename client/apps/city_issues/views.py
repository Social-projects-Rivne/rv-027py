"""
Django views
"""
# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from city_issues.models import Issues


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


def map_page_view(request):
    """Map page"""
    return render(request, 'map_page.html')


def get_issue_data(request, issue_id):
    data = serializers.serialize("json", Issues.objects.filter(pk=issue_id))
    return JsonResponse(data, safe=False)


def get_all_issues_data(request):
    data = serializers.serialize("json", Issues.objects.all())
    return JsonResponse(data, safe=False)
