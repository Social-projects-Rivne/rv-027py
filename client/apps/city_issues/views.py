"""
Django views
"""
# -*- coding: utf-8 -*-
import json
from django.views.generic.base import TemplateView
from django.template import loader
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from city_issues.models import Issues


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


def map_page_view(request):
    """Map page"""

    data = serializers.serialize("json", Issues.objects.all())

    context = {
        'data': data, }

    template = loader.get_template('map_page.html')

    return HttpResponse(template.render(context, request))


def get_issue_data(request, issue_id):
    data = serializers.serialize("json", Issues.objects.filter(pk=issue_id))
    return JsonResponse(data, safe=False)
