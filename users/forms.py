from django import forms
from django.contrib.auth.models import User
from .models import Profile
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['motto','about_yourself','profile_pic','q1','q2','q3','q4']