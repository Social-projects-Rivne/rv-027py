"""
Django views
"""
# -*- coding: utf-8 -*-
import json
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse, HttpResponse
from django.core import serializers
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
