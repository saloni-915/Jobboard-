from django import forms
from .models import Job
from .models import Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "location", "salary", "job_type"]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["full_name", "email", "phone", "bio", "cover_letter", "resume"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "cover_letter": forms.Textarea(attrs={"rows": 4}),
        }
