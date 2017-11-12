"""
Django views
"""
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"
