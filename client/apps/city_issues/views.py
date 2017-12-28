"""
Django views
"""
# -*- coding: utf-8 -*-
import json
import os.path

from datetime import date, datetime, time
import operator

from django import forms
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.postgres.search import SearchVector
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import make_aware
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse

from city_issues.models import Attachments, Issues, IssueHistory, User, \
    Comments, Category
from city_issues.forms.forms import (EditIssue, IssueFilter, IssueForm,
                                     IssueFormEdit, IssueSearchForm,
                                     EditUserForm, CommentsOnMapForm,
                                     IssueFormEditWithoutStatus,
                                     InternalCommentsForm, ModEditForm)
from city_issues.mixins import LoginRequiredMixin
from city_issues.thumbnails import create_thumbnail

ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"

    def get(self, request):
        return redirect("map")


class UserProfileView(View):
    """User profile page"""
    form_class = EditUserForm
    form_comments_class = InternalCommentsForm
    success_url = 'user_profile'
    template_name = 'user/user.html'

    def get(self, request):
        user = request.user
        user_issues = Issues.objects.filter(user_id=user.id)
        form = self.form_class(instance=User.objects.get(id=user.id))

        return render(request, self.template_name, {'user': user,
                                                    'user_issues': user_issues,
                                                    'form': form,
                                                    'comments_form': self.form_comments_class})

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        form = EditUserForm(data=request.POST, instance=request.user)

        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.alias = form.cleaned_data['alias']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['confirm_password'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Changes successfully saved')

        else:
            return render(request, self.template_name,
                          {'form': form, 'has_error': 'error'})

        return redirect(self.success_url)

    @classmethod
    def get_internal_comments(cls, request, issue_id):
        internal_comments = Comments.objects.filter(issue_id=issue_id,
                                                    status='internal').select_related(
            "user_id").values('comment', 'user_id', 'user__alias',
                              'date_public')

        return JsonResponse({'comments': list(internal_comments)})

    @classmethod
    def store_internal_comments(cls, request, issue_id):
        form = UserProfileView.form_comments_class(request.POST)

        if form.is_valid():
            comment = Comments()
            comment.comment = form.cleaned_data['comment']
            comment.issue_id = issue_id
            comment.user_id = request.user.id
            comment.status = 'internal'
            comment.date_public = datetime.now()
            comment.save()

            return JsonResponse({'answer': 'success'})
        else:
            return JsonResponse(form.errors.as_json(), status=400, content_type='application/json', safe=False)


class IssueCreate(CreateView):
    """Create new issue"""
    MAX_FILE_SIZE = 5242880

    model = Issues
    form_class = IssueForm
    template_name = 'issues/issues.html'
    success_url = 'map'

    def form_valid(self, form):
        form.instance.user = self.request.user
        issue = form.save(commit=True)

        if form.files:
            self.save_files(form, form.files.getlist('files'), issue)

        self.save_issue_history(issue, form.instance.user)
        messages.success(self.request, 'Issue was successfully saved')
        return super(IssueCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(IssueCreate, self).form_invalid(form)

    def save_files(self, form, files, issue):
        for issue_file in files:
            if issue_file._size > self.MAX_FILE_SIZE:
                messages.error(self.request, 'Max file size : 5MB')
                return super(IssueCreate, self).form_valid(form)
            else:
                attachment = Attachments()
                attachment.issue = issue
                attachment.image_url = issue_file
                attachment.save()
                create_thumbnail(issue_file, issue.title,
                                 attachment.image_url.url)

    def save_issue_history(self, issue, user):
        issue_history = IssueHistory()
        issue_history.issue = issue
        issue_history.user = user
        issue_history.save()


def map_page_view(request):
    """Map page"""
    form = IssueFilter()
    if request.user.is_anonymous():
        form.fields.pop('show_deleted')
        form.fields.pop('show_on_moderation')
        form.fields.pop('show_new')
        form.fields.pop('show_pending_close')

    if request.user.is_authenticated() and request.user.role.id not in (
            ROLE_ADMIN, ROLE_MODERATOR):
        form.fields.pop('show_deleted')

    comment_form = CommentsOnMapForm()
    return render(request, 'map_page.html',
                  {'form': form, 'comment_form': comment_form})


def get_issue_data(request, issue_id):
    """Returns single issue record as json"""
    single_issue = Issues()
    data = json.dumps(single_issue.get_issue_data_by_id(request, issue_id))
    return JsonResponse(data, safe=False)


def get_all_issues_data(request):
    """Returns all issues records as json with possible filter."""
    all_issues = Issues()
    role_based_query = all_issues.get_role_based_query(request)
    role_based_query_default_show = role_based_query.filter(
        status__in=["open", "new", "on moderation"])

    data = serializers.serialize(
        "json",
        role_based_query_default_show)

    form = IssueFilter(request.GET)

    if form.is_valid() and form.data.get('filter'):
        query = all_issues.issue_filter(form, role_based_query)
        data = serializers.serialize("json", query)

    return JsonResponse(data, safe=False)


class CheckIssues(ListView, FormView):
    """A list of issues"""
    form_class = IssueSearchForm
    template_name = 'issues_list.html'
    model = Issues
    context_object_name = 'issues_list'
    paginate_by = 8

    def get_queryset(self):
        """Adds sorting"""
        queryset = super(CheckIssues, self).get_queryset()
        order_by = self.request.GET.get('order_by')
        search = self.request.GET.get('search')

        if search:
            query_list = search.split()
            queryset = queryset.filter(
                reduce(operator.or_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.or_, (Q(description__icontains=q)
                                      for q in query_list))
            )
        if order_by in ('title', 'status', 'user', 'category', 'open_date'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == 'v_v':
                queryset = queryset.reverse()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CheckIssues, self).get_context_data(**kwargs)
        context['issues_range'] = range(context["paginator"].num_pages)
        return context


class UpdateIssue(IssueCreate, UpdateView):
    """Edit issue from map."""
    model = Issues
    form_class = IssueFormEdit
    template_name = 'edit_issue.html'
    success_url = '/map/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated() and (
                (self.request.user.role.id in (ROLE_ADMIN, ROLE_MODERATOR)) or
                (obj.user == self.request.user)):
            if self.request.user.role.id not in (ROLE_ADMIN, ROLE_MODERATOR):
                self.form_class = IssueFormEditWithoutStatus
            return super(UpdateIssue, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied("You are not allowed to edit this issue")


class DetailedIssue(DetailView):
    """Detailed issue"""
    template_name = 'issue_detailed.html'
    model = Issues


class CommentIssues(LoginRequiredMixin, CreateView):
    """Comment issue"""
    template_name = 'issue_detailed.html'
    fields = ['comment']

    def get_queryset(self):
        self.issue = get_object_or_404(Issues, pk=self.kwargs['pk'])
        return Comments.objects.filter(issue=self.issue)

    def get_context_data(self, **kwargs):
        context = super(CommentIssues, self).get_context_data(**kwargs)
        context['object'] = Issues.objects.get(pk=self.kwargs['pk'])
        context['attachment_list'] = Attachments.objects.filter(issue=self.issue)
        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        issue = Issues.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(pk=self.request.user.id)
        form.issue = issue
        form.user = user
        form.save()
        return redirect(
            reverse('issue-comment', kwargs={'pk': self.kwargs['pk']}))

    def form_invalid(self, form):
        return super(CommentIssues, self).form_invalid(form)


def delete_attachment(request):
    attachment_id = request.POST.get('attachment-id')
    attachment = Attachments.objects.get(id=attachment_id)
    attachment.delete()

    messages.success(request, 'Attachment successfully deleted')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def post_comment(request, issue_id):
    if request.user.is_authenticated():
        form = CommentsOnMapForm(request.POST)

        if form.is_valid():
            issue = Issues()
            list_of_comments_statuses = issue.get_actions_list(
                request, issue_id)['list_of_comments_statuses']
            comment_form_status = form.cleaned_data.get('status')
            if comment_form_status and comment_form_status in list_of_comments_statuses:
                comment = Comments()
                comment.comment = form.cleaned_data.get('comment')
                comment.user = request.user
                comment.status = comment_form_status
                comment.issue = Issues.objects.get(pk=issue_id)
                comment.date_public = datetime.now()
                comment.save()

                comments_list = Comments()
                comments_query = comments_list.get_comments(
                    issue_id, list_of_comments_statuses)

                data = json.dumps(comments_query)
                return JsonResponse(data, safe=False)

    raise PermissionDenied("You are not allowed to comment without login")


def issue_action(request, issue_id):
    """Makes actions with issues"""
    if request.user.is_authenticated():
        issue = Issues()
        list_of_actions = issue.get_actions_list(
            request, issue_id)['list_of_actions']
        action = request.POST.get('action')
        if action and action in list_of_actions:
            changing_issue = Issues.objects.get(pk=issue_id)
            changing_issue.status = action
            changing_issue.save()
            return JsonResponse({'result': 'success'}, safe=False)

    raise PermissionDenied("You are not allowed to change issue")


def mod_list_panel(request):
    """ A moderator list of issues"""
    if request.user.is_superuser or request.user.is_staff:
        issues_list = Issues.objects.order_by('-open_date')
        context = {'title': 'Moderator Panel:'}

        order_by = request.GET.get('order_by', '')
        if order_by in ('title', 'status', 'user', 'category', 'open_date', 'delete_date'):
            issues_list = issues_list.order_by(order_by)
            if request.GET.get('reverse', '') == '1':
                issues_list = issues_list.reverse()

        query = request.GET.get('q')
        if query is not None:
            issues_list = Issues.objects.annotate(search=SearchVector('title', 'status', 'category__category',
                                                                      config='english')).filter(search=query)
            context['last_query'] = '?q=%s' % query

        current_page = Paginator(issues_list, 10)
        page = request.GET.get('page')
        try:
            context['issues_list'] = current_page.page(page)
        except PageNotAnInteger:

            context['issues_list'] = current_page.page(1)
        except EmptyPage:

            context['issues_list'] = current_page.page(current_page.num_pages)

        if page == '1':
            return redirect('modpanel', permanent=True)
    else:
        context = {'title': 'You have not permission to this page'}
        return render(request, 'mod/permission.html', context)
    return render(request, 'mod/mod_list.html', context)


def mod_edit_issue(request, pk=None):
    """A moderator edit issues"""
    issues = get_object_or_404(Issues, pk=pk)
    form = ModEditForm(request.POST or None, instance=issues)
    if form.is_valid():
        issues = form.save(commit=False)
        issues.save()
        messages.success(request, "Successfully Update")
        return HttpResponseRedirect(issues.get_absolute_url())
    context = {
        "title": issues.title,
        "issue": issues,
        "form": form,
    }
    return render(request, "mod/mod_edit.html", context)


def delete_issue(request, pk):
    """Route for deleting issue."""
    issue = get_object_or_404(Issues, pk=pk)
    if request.method == "POST":
        issue.mod_delete()
        issue.save()
        return redirect("modpanel")
    context = {
        "issue": issue
    }
    return render(request, "mod/confirm_delete.html", context)


def restore_issue(request, pk):
    """Route for restoring issue."""
    issue = get_object_or_404(Issues, pk=pk)
    if request.method == "POST":
        issue.mod_restore()
        issue.save()
        return redirect("modpanel")
    context = {
        "issue": issue
    }
    return render(request, "mod/confirm_restore.html", context)


def comment_delete(request, issue_id, comment_id):
    if request.user.is_authenticated() and request.user.role.id in (
            ROLE_ADMIN, ROLE_MODERATOR):
        comment = Comments.objects.get(pk=comment_id)
        comment.pre_deletion_status = comment.status
        comment.status = "deleted"
        comment.save()
        return redirect(reverse('issue-comment', args=[issue_id]))
    raise PermissionDenied("You are not allowed to delete comments")


def comment_restore(request, issue_id, comment_id):
    if request.user.is_authenticated() and request.user.role.id in (
            ROLE_ADMIN, ROLE_MODERATOR):
        comment = Comments.objects.get(pk=comment_id)

        comment.status = 'public'
        if comment.pre_deletion_status:
            comment.status = comment.pre_deletion_status
        comment.save()
        return redirect(reverse('issue-comment', args=[issue_id]))
    raise PermissionDenied("You are not allowed to delete comments")


def imgResponse(request, path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    raise Http404
