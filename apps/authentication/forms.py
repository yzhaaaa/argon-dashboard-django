# -*- coding: utf-8 -*-
"""
    Copyright (c) 2019 - present AppSeed.us
    """

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, UserCredentials


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )


class SignUpFormInfo(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'middlename',
                  'lastname', 'address', 'date_of_birth']

        widgets = {
            'firstname': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }),
            'middlename': forms.TextInput(attrs={
                'placeholder': 'Middle Name',
                'class': 'form-control'
            }),
            'lastname': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Address',
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Date of Birth',
                'class': 'form-control'
            }),
        }


class SignUpFormCredentials(forms.ModelForm):
    class Meta:
        model = UserCredentials
        fields = ['username', 'email_address', 'password_hash']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }),
            'email_address': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }),
            'password_hash': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }),
        }
