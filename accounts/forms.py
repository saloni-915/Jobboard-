from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from jobs.models import Company
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=UserProfile.role_choices
    )
    class Meta:
        model = User
        fields = ['username','email','password1','password2','role']


    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            UserProfile.objects.create(
                user = user,
                role = self.cleaned_data['role']
            )

        return user 

#----------profile update form-----------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','phone','profile_picture','skills', 'linkedin_url', 'github_url', 'experience']

#-----------company form--------

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company  # ← change karo
        fields = ['name', 'logo', 'website', 'description','location', 'company_size', 'industry', 'founded_year'] 

        