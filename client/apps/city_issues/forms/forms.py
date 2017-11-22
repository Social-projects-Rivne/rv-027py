from django import forms

from city_issues.models.issues import Issues, Category


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issues
        fields = ['description', 'category', 'location_lat', 'location_lon', 'name']

    name = forms.CharField(
        max_length=350,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        max_length=350,
        min_length=5,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
    )

    location_lat = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
    )

    location_lon = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )

    file = forms.FileField(
        widget=forms.FileInput()
    )
