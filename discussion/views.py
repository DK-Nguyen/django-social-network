from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DiscussionCreationForm, DiscussionUpdateForm
from .models import Discussion, DiscussionComment
from django.contrib.auth.decorators import login_required

from .models import *


@login_required
def discussions(request):
    all_discussions = Discussion.objects.all()
    context = {
        'discussions': all_discussions
    }
    return render(request, 'discussion/discussion_list.html', context=context)


@login_required
def new_discussion(request):
    if request.method == 'POST':
        form = DiscussionCreationForm(request.POST)
        if form.is_valid():
            m = form.save()
            messages.success(request, 'Discussion has been created')
            return redirect(m.get_absolute_url())
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
def discussion(request, discussion_id):
    current_discussion = Discussion.objects.get(id=discussion_id)
    comments = DiscussionComment.objects.filter(discussion=current_discussion)
    participants = DiscussionParticipant.objects.filter(discussion=current_discussion)
    context = {
        'discussion': current_discussion,
        'comments': comments,
        'participants': participants
    }

    return render(request, 'discussion/discussion_details.html', context)