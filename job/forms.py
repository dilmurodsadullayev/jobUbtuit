from django import forms
from .models import Document


class DocumentCreateForm(forms.ModelForm):
    birth_date = forms.DateField(
        # input_formats=['%m/%d/%y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',

            'type': 'date'
        })
    )
    class Meta:
        model = Document
        fields = ["vacancy","full_name","birth_date", "phone_number", "education_level","passport", "objective", "diploma", "language_certificate","benefits"]

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        return birth_date.strftime('%Y-%m-%d')