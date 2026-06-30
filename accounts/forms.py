from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from jobs.models import Company

from .models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    role = forms.ChoiceField(choices=UserProfile.role_choices)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "role",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label,
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=self.cleaned_data["role"])

        return user


# ----------profile update form-----------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "phone",
            "profile_picture",
            "skills",
            "linkedin_url",
            "github_url",
            "experience",
        ]


# -----------company form--------
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "logo",
            "website",
            "description",
            "location",
            "company_size",
            "industry",
            "founded_year",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label,
            })
