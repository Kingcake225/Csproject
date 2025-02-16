from django import forms
from .models import CV

class CVUploadForm(forms.ModelForm):
    personal_statement = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    custom_message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )

    class Meta:
        model = CV
        fields = ['name', 'mobile_number', 'position', 'education_level', 
                 'education_discipline', 'personal_statement', 'custom_message', 'pdf_file']
