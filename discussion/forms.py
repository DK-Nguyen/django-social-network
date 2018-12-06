from django import forms
from .models import *
from django.core.exceptions import ValidationError


class DiscussionCreationForm(forms.Form):
    '''A form that is used to create a new discussion'''
    title = forms.CharField(required=True, max_length=150, label="Discussion title")
    description = forms.CharField(required=False, label='Discussion description')

    def clean(self):
        '''Makes sure the form is valid'''
        super(forms.Form, self).clean()

        if self.cleaned_data.get('title') == '':
            raise ValidationError("Title is mandatory")

    class Meta:
        model = Discussion
        fields = ['title', 'description']


class DiscussionUpdateForm(forms.ModelForm):
    '''A form that is used to update an existing discussion's details'''
    title = forms.CharField(required=True, max_length=150, label="Discussion title")
    description = forms.CharField(required=False, label='Discussion description')

    class Meta:
        model = Discussion
        fields = ['title', 'description']


class DiscussionCommentForm(forms.ModelForm):
    '''A form that is used to create a new comment to a discussion'''
    content = forms.CharField(required=True)

    class Meta:
        model = DiscussionComment
        fields = [ 'content' ]
