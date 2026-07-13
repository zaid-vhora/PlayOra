from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_modules.userapp import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_image', 'date_of_birth', 'gender', 'city', 'pincode']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }