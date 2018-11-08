from django.db import models
from django.conf import settings


class Discussion(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/discussion/%i/" % self.id


class DiscussionComment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_time = models.DateTimeField(auto_now_add=True)


class DiscussionParticipant(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
















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
