import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    name = forms.CharField(required=True, label='Your name')
    username = forms.CharField(required=True, min_length=4, max_length=30)
    email = forms.EmailField(required=True)
    phone_number = forms.RegexField(required=True, regex=r'^\+?1?\d{9,15}$')
    name = forms.CharField(required=True, label='Your name')
    address = forms.CharField(required=True, label='Your address')
    password1 = forms.CharField(required=True, min_length=8, max_length=30, label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label="Confirm", widget=forms.PasswordInput())
    administrator = forms.NullBooleanField(label="Apply as Administrator", widget=forms.CheckboxInput(), required=False)

    def clean(self):
        super(UserCreationForm, self).clean()

        # Custom checks for email uniqueness
        if User.objects.filter(email=self.cleaned_data.get('email')).count() > 0:
            raise ValidationError("E-mail already registered")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
