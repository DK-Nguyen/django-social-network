from django import forms
from .models import *
from django.core.exceptions import ValidationError


class EventCreationForm(forms.Form):
    name = forms.CharField(required=True, max_length=150, label="Event name")
    description = forms.CharField(required=False, label='Event description')

    def clean(self):
        super(forms.Form, self).clean()

        if self.cleaned_data.get('title') == '':
            raise ValidationError("Title is mandatory")

    class Meta:
        model = Event
        fields = ['name', 'description']


class EventUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=150, label="Event name")
    description = forms.CharField(required=False, label='Discussion description')

    class Meta:
        model = Event
        fields = ['name', 'description']

