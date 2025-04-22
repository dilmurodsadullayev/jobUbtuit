from django import forms
from .models import Document
from .models import CustomUser



class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["vacancy", "education_level","passport", "objective", "diploma", "language_certificate","benefits"]


class CustomUserCreate(forms.ModelForm):
    birth_date = forms.DateField(
        # input_formats=['%m/%d/%y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',

            'type': 'date'
        })
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "birth_date", "phone_number"]

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        return birth_date.strftime('%Y-%m-%d')



class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'phone_number',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_birth_date(self):
        birthdate = self.cleaned_data['birthdate']
        return birthdate.strftime('%Y-%m-%d')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # 👈 Muhim qadam
        if commit:
            user.save()
        return user