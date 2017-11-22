"""
Django views
"""
# -*- coding: utf-8 -*-

from django.views.generic import FormView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib import auth, messages

from forms import RegistrationForm, LoginForm


class RegistrationView(SuccessMessageMixin, FormView):
    """View for registering new users"""
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = "You've been successfully registered"

    def get_form_kwargs(self):
        """Initial form"""
        kwargs = super(RegistrationView, self).get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def form_invalid(self, form, **kwargs):
        """Open the registration form again to correct errors"""
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        """Create new user"""
        response = super(RegistrationView, self).form_valid(form)
        form.save()
        return response


class LoginView(SuccessMessageMixin, FormView):
    """Display the login page."""
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    success_message = "You have successfully logged in"

    def form_invalid(self, form):
        """The authorization form is not valid."""
        response = super(LoginView, self).form_invalid(form)
        messages.error(self.request, 'Please, check your login/password')

        return response

    def form_valid(self, form):
        """The authorization form is valid - authorize this user."""

        # Authenticate user.
        user = auth.authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],)

        # If the user exists - logged.
        if user is not None:
            auth.login(self.request, user)

        response = super(LoginView, self).form_valid(form)
        return response


class LogoutView(RedirectView):
    """..."""
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        """Run logout and get redirect url"""
        # Logout.
        auth.logout(self.request)

        # Generate redirect url.
        next = reverse('home')
        if self.request.method == 'GET':
            _next = self.request.GET.get('next', None)
            next = _next if _next else next

        return next


class HomePageView(TemplateView):
    """Home page"""
    template_name = "home_page.html"
