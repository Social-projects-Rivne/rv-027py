"""Forms models"""
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from city_issues.models.issues import Issues, Category, Comments
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
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}))

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}))

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
        required=False, )


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

    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        user = User.objects.get(id=self.instance.id)

        if current_password or new_password or confirm_password:
            self.check_passwords(user, current_password, new_password,
                                 confirm_password)

        return cleaned_data

    def check_current_password(self, user, current_password):
        if not user.check_password(current_password):
            self._errors['Current password'] = self.error_class(
                ['Incorrect current password'])
            del self.cleaned_data['confirm_password']
            return False
        else:
            return True

    def check_passwords(self, user, current_password, new_password,
                        confirm_password):
        if not self.check_current_password(user, current_password):
            return None

        if (confirm_password or new_password) and (
                new_password != confirm_password):
            self._errors['Confirm password'] = self.error_class(
                ['Passwords do not match.'])
            del self.cleaned_data['confirm_password']

        if not new_password and not confirm_password and self.check_current_password(user, current_password):
            self._errors['New password, confirm password'] = self.error_class(
                ['Fields is required'])


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
        required=False,
        initial='title')
    reverse = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)
    page = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False)


class IssueFormEdit(IssueForm):
    files = None


class CommentsOnMapForm(forms.Form):
    """Map comments form."""

    comment = forms.CharField(
        required=False,
        min_length=1,
        max_length=350,
        widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Comments
        fields = ['comment']
