from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date', 'location', 'website']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Аватар'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Біографія', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата народження', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місцезнаходження'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Веб-сайт'}),
        }