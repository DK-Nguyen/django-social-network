from django import forms
from .models import Status, StatusComment
from django.core.exceptions import ValidationError


class StatusCreationForm(forms.Form):
    content = forms.CharField(required=True, label='What is on your mind',)
    owner = "Owner"

    def clean(self):
        super(forms.Form, self).clean()

        if self.cleaned_data.get('content') == '':
            raise ValidationError("Status content is mandatory")

    class Meta:
        model = Status
        fields = ['content']


class StatusCommentForm(forms.Form):
    content = forms.CharField(required=True)

    class Meta:
        model = StatusComment
        fields = ['content']

