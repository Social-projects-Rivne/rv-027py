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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from city_issues.views import (
    edit_issue_view, get_all_issues_data, get_issue_data,
    HomePageView, map_page_view, IssueCreate, UserProfileView)


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^map/$', map_page_view, name='map'),
    url(r'^map/getissuebyid/(?P<issue_id>[0-9]+)$',
        get_issue_data, name='issue_data'),
    url(r'^map/getissuesall/$', get_all_issues_data, name='all_issues'),
    url(r'^add-issue', login_required(IssueCreate.as_view()), name='create_issue'),
    url(r'^editissue/(?P<issue_id>[0-9]+)$', edit_issue_view, name='edit_issue'),

    # registration and authorization views
    url(r'^accounts/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^accounts/profile/(?P<user_id>[0-9]+)$', UserProfileView.as_view(), name='user_profile'),
    url(r'^accounts/', include('registration.backends.simple.urls', namespace='accounts')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
