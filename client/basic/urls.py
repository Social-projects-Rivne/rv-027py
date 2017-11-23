"""basic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from city_issues.views import (
    edit_issue_view, get_all_issues_data, get_issue_data,
    HomePageView, map_page_view, IssueCreate)



urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^map/$', map_page_view, name='map'),
    url(r'^map/getissuebyid/(?P<issue_id>[0-9]+)$',
        get_issue_data, name='issue_data'),
    url(r'^map/getissuesall/$', get_all_issues_data, name='all_issues'),
    url(r'^add-issue', IssueCreate.as_view(), name='create_issue'),
    url(r'^editissue/(?P<issue_id>[0-9]+)$', edit_issue_view, name='edit_issue'),
]
