"""Forms models"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms

from django.forms import (
    CharField, FloatField, ModelChoiceField, ModelForm,
    Textarea, TextInput)

from city_issues.models.issues import Issues, Category


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issues
        fields = ['description', 'category', 'location_lat', 'location_lon', 'title']

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
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )

    location_lon = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )

    file = forms.FileField(
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
