"""
Django views
"""
# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView

from city_issues.models import Attachments, Issues, Category
from city_issues.forms.forms import EditIssue, IssueForm


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"


class IssueCreate(CreateView):
    model = Issues
    form_class = IssueForm
    template_name = 'issues/issues.html'
    success_url = 'add-issue'

    def form_valid(self, form):
        issue = form.save(commit=True)

        file = form.cleaned_data['file']
        if file:
            self.save_file(form, file, issue)

        messages.success(self.request, 'Issue was successfully saved')
        return super(IssueCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to save')
        return super(IssueCreate, self).form_invalid(form)

    def save_file(self, form, file, issue):
        if file._size > 5242880:
            messages.error(self.request, 'Max file size : 5MB')
            return super(IssueCreate, self).form_valid(form)
        else:
            attachment = Attachments()
            attachment.issue = issue
            attachment.image_url = file
            attachment.save()


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


class CheckIssues(ListView):
    """A list of issues"""
    template_name = 'issues_list.html'
    model = Issues
    context_object_name = 'issues_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(CheckIssues, self).get_context_data(**kwargs)
        context['issues_range'] = range(context["paginator"].num_pages)
        return context
