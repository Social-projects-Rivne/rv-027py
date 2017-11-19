from django import forms

# from models.issues import Category


class IssueForm(forms.Form):

    description = forms.CharField(
        required=True,
        max_length=350,
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
    )

    latitude = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )

    longitude = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )