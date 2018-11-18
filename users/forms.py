from django import forms
from users.models import SiteUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    address = forms.CharField(required=True, label='Your address')
    first_name = forms.CharField(required=True, max_length=150, label="Your First Name")
    last_name = forms.CharField(required=True, max_length=150, label="Your Last Name")
    email = forms.EmailField(required=True, label="Your Email")
    phone_number = forms.CharField(label="Your phone number", required=True)
    bio = forms.CharField(required=False, label='Tell us a bit about yourself')

    def clean(self):
        super(UserCreationForm, self).clean()

        if self.cleaned_data.get('email') == '':
            raise ValidationError("Email cannot be empty!")

        # Custom checks for first name and lastname
        if self.cleaned_data.get('first_name') == '' or self.cleaned_data.get('last_name') == '':
            raise ValidationError("Name cannot be empty")

        # Custom checks for email uniqueness
        if SiteUser.objects.filter(email=self.cleaned_data.get('email')).count() > 0:
            raise ValidationError("E-mail already registered")

    class Meta:
        model = SiteUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'address', 'phone_number', 'bio')


class UserUpdateForm(forms.ModelForm):
    address = forms.CharField(required=True, label='Your new Address')
    first_name = forms.CharField(required=True, max_length=150, label="Your new First Name")
    last_name = forms.CharField(required=True, max_length=150, label="Your new Last Name")
    phone_number = forms.CharField(label="Your new phone number", required=True)
    bio = forms.CharField(required=False, label='Write something new about yourself')

    class Meta:
        model = SiteUser
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'bio']
