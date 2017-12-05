"""Forms models"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms

from django.forms import (
    CharField, DateInput, FloatField, ModelChoiceField, ModelForm,
    Textarea, TextInput)

from city_issues.models.issues import Issues, Category
from city_issues.models.users import User


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issues
        fields = ['description', 'category',
                  'location_lat', 'location_lon', 'title']

    title = forms.CharField(
        max_length=35,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        max_length=350,
        min_length=5,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
    )

    location_lat = forms.FloatField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )

    location_lon = forms.FloatField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )

    files = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*', 'multiple': True})
    )


class EditIssue(ModelForm):
    """Edit issue form."""
    title = CharField(
        min_length=5,
        max_length=50,
        widget=TextInput({'size': 50}),
        required=True)

    description = CharField(
        min_length=5,
        max_length=350,
        widget=Textarea(attrs={'rows': 5, 'class': 'issue_description'}))

    category = ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None
    )

    location_lat = FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])

    location_lon = FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)])

    class Meta:
        model = Issues
        fields = ['title', 'category', 'location_lat',
                  'location_lon', 'description']


class IssueFilter(forms.Form):
    """Issue filter form on map."""
    date_from = forms.DateField(
        required=True,
        widget=DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(
        required=True,
        widget=DateInput(attrs={'type': 'date'}))


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'alias', 'email']
    #
    # def clean_email(self):
    #     alias = self.cleaned_data["alias"]
    #     email = self.cleaned_data["email"]
    #     users = User.objects.filter(email__iexact=email).exclude(
    #         alias__iexact=alias)
    #     if users:
    #         raise forms.ValidationError(
    #             'User with that email already exists.')
    #     return email.lower()

    name = forms.CharField(
        max_length=25,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    alias = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        max_length=50,
        min_length=4,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    current_password = forms.CharField(
        required=False,
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password = forms.CharField(
        required=False,
        max_length=50,
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    confirm_password = forms.CharField(
        required=False,
        max_length=50,
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
