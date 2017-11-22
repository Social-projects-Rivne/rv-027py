"""Forms models"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import (
    CharField, FloatField, ModelChoiceField, ModelForm,
    Textarea, TextInput)

from city_issues.models import Issues, Category


class EditIssue(ModelForm):
    """Edit issue form."""
    name = CharField(
        min_length=5,
        max_length=50,
        widget=TextInput({'size': 50}),
        required=True)

    description = CharField(
        min_length=5,
        max_length=50,
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
        fields = ['name', 'category', 'location_lat',
                  'location_lon', 'description']
