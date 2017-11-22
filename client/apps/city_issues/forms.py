from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q


class RegistrationForm(forms.Form):
    """Form to register users."""

    name = forms.CharField(
        label='Name',
    )
    alias = forms.CharField(
        required=False,
        label='Nickname',
    )
    email = forms.EmailField(
        label='E-mail',
    )
    avatar = forms.ImageField(
        required=False,
        label='Avatar',
    )
    password = forms.CharField(
        label='Password',
        min_length=3,
        max_length=30,
    )
    password_confirm = forms.CharField(
        min_length=3,
        required=False,
        label='Confirm password',
    )

    def __init__(self, *args, **kwargs):
        """Init profile account form."""
        self.request = kwargs.pop('request', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """The email field validator."""
        email = self.cleaned_data['email']

        User = get_user_model()
        query = Q(email__iexact=email)
        existing = User.objects.filter(query)

        if existing.exists():
            raise forms.ValidationError(
                'User with such email already exists!'
            )

        return email

    def save(self):
        """Create new user and his profile."""
        # Client model.
        user = get_user_model()
        name = self.cleaned_data.get('name')
        alias = self.cleaned_data.get('alias')
        email = self.cleaned_data.get('email')
        avatar = self.cleaned_data.get('avatar')
        password = self.cleaned_data.get('password')

        # Create new user.
        client = user.objects.create_user(name=name, email=email,
                                          password=password)
        client.alias = alias
        client.avatar = avatar
        client.save()


class LoginForm(forms.Form):
    """The form of the user's authorization"""
    email = forms.EmailField(
        label='E-mail',
    )
    password = forms.CharField(
        min_length=3,
        label='Password',
    )

    def clean(self):
        """The user must be registered"""
        data = super(LoginForm, self).clean()
        email = data.get('email')
        password = data.get('password')

        # Check user rights.
        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError('Access denied')

        return data
