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
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

from city_issues.views import (
    CheckIssues, DetailedIssue, delete_attachment, get_all_issues_data, get_issue_data,
    HomePageView, map_page_view, IssueCreate, UserProfileView, UpdateIssue, CommentIssues,
    post_comment, issue_action, comment_delete, comment_restore, mod_list_panel, mod_edit_issue,
    delete_issue, restore_issue, imgResponse, mod_comment)


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^issues/$', CheckIssues.as_view(), name='issues'),
    url(r'^issue-comment/(?P<pk>[0-9]+)/$', CommentIssues.as_view(), name='issue-comment'),
    url(r'^issue/(?P<pk>\d+)/$', DetailedIssue.as_view(), name='issue'),
    url(r'^delete-attachment/$', delete_attachment, name='delete-attachment'),
    url(r'^postcomment/(?P<issue_id>[0-9]+)/$', post_comment, name='post-comment'),
    url(r'^issueaction/(?P<issue_id>[0-9]+)/$', issue_action, name='issue-action'),
    url(r'^modpanel/$', mod_list_panel, name='modpanel'),
    url(r'^modpanel/(?P<pk>\d+)/edit/$', mod_edit_issue, name='mod_edit'),
    url(r'^modpanel/(?P<pk>\d+)/delete/$', delete_issue, name='delete_issue'),
    url(r'^modpanel/(?P<pk>\d+)/restore/$', restore_issue, name='restore_issue'),
    url(r'^modcomment/(?P<pk>\d+)/$', mod_comment, name='modcomment'),
    url(r'^deletecomment/(?P<issue_id>[0-9]+)/(?P<comment_id>[0-9]+)/$', comment_delete, name='comment-delete'),
    url(r'^restorecomment/(?P<issue_id>[0-9]+)/(?P<comment_id>[0-9]+)/$', comment_restore, name='comment-restore'),
    url(r'^internal-comments/(?P<issue_id>[0-9]+)/$', UserProfileView.get_internal_comments, name='internal-comment'),
    url(r'^store/internal-comments/(?P<issue_id>[0-9]+)/$', UserProfileView.store_internal_comments, name='store-internal-comment'),

    url(r'^map/$', map_page_view, name='map'),
    url(r'^map/getissuebyid/(?P<issue_id>[0-9]+)$',
        get_issue_data, name='issue_data'),
    url(r'^map/getissuesall/$', get_all_issues_data, name='all_issues'),
    url(r'^add-issue', login_required(IssueCreate.as_view()), name='create_issue'),
    url(r'^editissue/(?P<pk>[0-9]+)$', UpdateIssue.as_view(), name='edit_issue'),

    # registration and authorization views
    url(r'^accounts/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^accounts/profile/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^accounts/', include('registration.backends.simple.urls', namespace='accounts', )),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:
    urlpatterns.append(url(r'^media(?P<path>.*)$', imgResponse, name='media'))
