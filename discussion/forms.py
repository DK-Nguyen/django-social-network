from django import forms
from .models import *
from django.core.exceptions import ValidationError


FRIENDS_LIST = ["Erkki Esimerkki", "Kalle Kaveri", "Jonne Jonnela", "Yrjo Ystava"]


class DiscussionCreationForm(forms.Form):
    title = forms.CharField(required=True, max_length=150, label="Discussion title")
    description = forms.CharField(required=False, label='Discussion description')
    # participants = forms.MultipleChoiceField(choices=FRIENDS_LIST)
    owner = "Owner"
    # participants.append(owner)

    def clean(self):
        super(forms.Form, self).clean()

        if self.cleaned_data.get('title') == '':
            raise ValidationError("Title is mandatory")

    class Meta:
        model = Discussion
        fields = ['title', 'description']


class DiscussionUpdateForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=150, label="Discussion title")
    description = forms.CharField(required=False, label='Discussion description')

    class Meta:
        model = Discussion
        fields = ['title', 'description']

class DiscussionCommentForm(forms.ModelForm):
    content = forms.CharField(required=True)

    class Meta:
        model = DiscussionComment
        fields = [ 'content' ]
