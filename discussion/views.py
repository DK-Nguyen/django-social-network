from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *


@login_required
def discussions(request):
    return render(request, 'discussions.html')


@login_required
def new_discussion(request):
    return render(request, 'new_discussion.html')


@login_required
def discussion(request):
    return render(request, 'discussion.html')
