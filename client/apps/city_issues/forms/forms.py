from django import forms

from city_issues.models.issues import Attachments, Issues, Category


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issues
        fields = ['description', 'category', 'latitude', 'longitude', 'name']

    name = forms.CharField(
        max_length=350,
        min_length=3,
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )

    description = forms.CharField(
        max_length=350,
        min_length=5,
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
    )

    latitude = forms.FloatField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )

    longitude = forms.FloatField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )


class AttachmentForm(forms.ModelForm):

    class Meta:
        model = Attachments
        fields = ['issue', 'image_url']

    file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )