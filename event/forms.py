from django import forms
from .models import *
from django.core.exceptions import ValidationError


class EventCreateAndUpdateForm(forms.ModelForm):
    """This form is used to create and edit events
    """
    name = forms.CharField(required=True, max_length=150, label="Event name")
    description = forms.CharField(required=False, label='Discussion description')
    location = forms.CharField(required=False, label='Location (optional)')
    start_time = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'datepicker'
    }))
    end_time = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'datepicker'
    }))

    def clean(self):
        super(forms.ModelForm, self).clean()

        if self.cleaned_data.get('start_time') > self.cleaned_data.get('end_time'):
            raise ValidationError("End date should not be before start date")

    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_time', 'end_time']

