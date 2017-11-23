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
from django.conf.urls import include, url
from django.views.generic import RedirectView

from city_issues.views import HomePageView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    # registration and authorization views
    url(r'^accounts/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^accounts/profile/$', RedirectView.as_view(pattern_name='home'), name='success'),
    url(r'^accounts/', include('registration.backends.simple.urls', namespace='accounts')),
]
