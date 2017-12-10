"""Forms models"""
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

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


class EditIssue(forms.ModelForm):
    """Edit issue form."""
    title = forms.CharField(
        min_length=5,
        max_length=50,
        widget=forms.TextInput({'size': 50}),
        required=True)

    description = forms.CharField(
        min_length=5,
        max_length=350,
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'issue_description'}))

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None
    )

    location_lat = forms.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])

    location_lon = forms.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)])

    class Meta:
        model = Issues
        fields = ['title', 'category', 'location_lat',
                  'location_lon', 'description']


class IssueFilter(forms.Form):
    """Issue filter form on map."""
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    show_closed = forms.BooleanField(
        label="Closed only",
        required=False,
        initial=False,
        widget=forms.CheckboxInput())

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All categories",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    search = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max length 20 chars',
        }),
        required=False,)


class EditUserForm(forms.ModelForm):
    """Edit user form"""
    class Meta:
        model = User
        fields = ['name', 'alias', 'email']

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


class IssueSearchForm(forms.Form):
    """Issue search form."""
    search = forms.CharField(
        min_length=2,
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={
            'size': '60%'
        }),
        required=False)
    order_by = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)
    reverse = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)
    page = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False)


class IssueFormEdit(IssueForm):

    files = None
