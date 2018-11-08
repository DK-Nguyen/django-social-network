from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DiscussionCreationForm, DiscussionUpdateForm
from django.contrib.auth.decorators import login_required

from .models import *


@login_required
def discussions(request):
    return render(request, 'discussions.html')


@login_required
def new_discussion(request):
    if request.method == 'POST':
        form = DiscussionCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discussion has been created')
            return redirect(Discussion)
    else:
        form = DiscussionCreationForm()

    context = {
        'form': form,
    }

    return render(request, Discussion, context)


@login_required
def edit_discussion(request):
    if request.method == 'POST':
        form = DiscussionUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discussion has been updated')
            return redirect(Discussion)
    else:
        form = DiscussionUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, Discussion, context)


@login_required
def discussion(request):
    return render(request, Discussion)
