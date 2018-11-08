from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *


@login_required
def discussions(request):
    single_discussion = {
        'title': 'My test discussion',
        'description': 'My test discription which is much longer than the normal discussion',
        'author': {
            'name': request.user.name(),
            'profile_image': request.user.profile_picture.url
        },
        'number_of_comments': 10
    }
    context = {
        'discussions': [single_discussion, single_discussion]
    }
    return render(request, 'discussion/discussion_list.html', context=context)


@login_required
def new_discussion(request):
    return render(request, 'discussion/discussion_new.html')


@login_required
def discussion(request, discussion_id):
    return render(request, 'discussion/discussion_list.html')
