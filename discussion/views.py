from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from .forms import DiscussionCreationForm, DiscussionUpdateForm, DiscussionCommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from users.models import SiteUser
from gravatar.tags import gravatar_url

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
            cleaned_data = form.cleaned_data
            added_discussion = Discussion(
                title=cleaned_data.get('title'),
                description=cleaned_data.get('description'),
                owner=request.user
            )
            added_discussion.save()
            self_participation = DiscussionParticipant(
                participant=request.user,
                discussion=added_discussion
            )
            self_participation.save()
            messages.success(request, 'Discussion has been created')
            return redirect(added_discussion.get_absolute_url())
    else:
        form = DiscussionCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'discussion/discussion_new.html', context)


@login_required
def edit_discussion(request, discussion_id):
    discussion_to_update = Discussion.objects.get(id__exact=discussion_id)
    if request.method == 'POST':
        form = DiscussionUpdateForm(request.POST, instance=discussion_to_update)
        if form.is_valid():
            edited_discussion = form.save()
            messages.success(request, 'Discussion has been updated')
            return redirect(edited_discussion.get_absolute_url())
    else:
        form = DiscussionUpdateForm(instance=discussion_to_update)

    context = {
        'form': form,
    }

    return render(request, 'discussion/discussion_edit.html', context)


@login_required
def discussion(request, discussion_id):
    current_discussion = Discussion.objects.get(id=discussion_id)
    participants = DiscussionParticipant.objects.filter(discussion=current_discussion)
    find_user_participate = DiscussionParticipant.objects.filter(
        discussion=current_discussion,
        participant=request.user
    )
    is_owner = request.user == current_discussion.owner
    is_participating = len(find_user_participate) > 0
    context = {
        'discussion': current_discussion,
        'participants': participants,
        'is_participating': is_participating,
        'is_owner': is_owner
    }

    return render(request, 'discussion/discussion_details.html', context)


@login_required
@require_http_methods(["POST"])
def invite_participant(request, discussion_id, friend_id):
    try:
        friend = SiteUser.objects.get(id=friend_id)
        discussion = Discussion.objects.get(id=discussion_id)
        find_participant = DiscussionParticipant.objects.filter(participant=friend, discussion=discussion)
        if len(find_participant) > 0:
            return HttpResponseBadRequest('Friend is already in the discussion')
        new_participant = DiscussionParticipant(participant=friend, discussion=discussion)
        new_participant.save()
        return redirect(discussion.get_absolute_url())
    except SiteUser.DoesNotExist:
        return Http404('Friend not found')
    except Discussion.DoesNotExist:
        return Http404('Discussion not found')
    return HttpResponse('OK')


@login_required
def leave_discussion(request, discussion_id):
    try:
        discussion = Discussion.objects.get(id=discussion_id)
        participants = DiscussionParticipant.objects.filter(participant=request.user, discussion=discussion)
        if (len(participants) == 0):
            return Http404('Participant is not in this discussion!')
        for participant in participants:
            participant.delete()
        return redirect('/discussions')
    except SiteUser.DoesNotExist:
        return Http404('Friend not found')
    except DiscussionParticipant.DoesNotExist:
        return Http404('Participant not found')
    return HttpResponse('OK')


@login_required
@require_http_methods(["GET"])
def get_comments(request, discussion_id):
    try:
        current_discussion = Discussion.objects.get(id=discussion_id)
        comments = DiscussionComment.objects.filter(discussion=current_discussion)
        response = []
        for comment in comments:
            response.append({
                'id': comment.id,
                'content': comment.content,
                'created_time': comment.created_time.isoformat(),
                'commenter': {
                    'name': comment.commenter.name(),
                    'profile_picture': gravatar_url(comment.commenter.email, 20)
                },
                'can_delete': comment.commenter == request.user or request.user == current_discussion.owner
            })
        return JsonResponse({'comments': response})
    except Discussion.DoesNotExist:
        return Http404('Discussion not found')


@login_required
@require_http_methods(["POST"])
def post_comments(request, discussion_id):
    try:
        current_discussion = Discussion.objects.get(id=discussion_id)
        participants = DiscussionParticipant.objects.filter(discussion=current_discussion, participant=request.user)
        if len(participants) == 0:
            return HttpResponseForbidden('You cannot comment to this discussion!')
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            new_comment = DiscussionComment(
                content=form.cleaned_data.get('content'),
                commenter=request.user,
                discussion=current_discussion
            )
            new_comment.save()
            return HttpResponse('OK')
        return HttpResponseBadRequest('Not a valid comment')
    except Discussion.DoesNotExist:
        return Http404('Discussion not found')


@login_required()
@require_http_methods(["DELETE"])
def delete_comment(request, discussion_id, comment_id):
    try:
        current_discussion = Discussion.objects.get(id=discussion_id)
        current_comment = DiscussionComment.objects.get(id=comment_id)
        commenter = current_comment.commenter
        discussion_owner = current_discussion.owner
        if request.user == commenter or request.user == discussion_owner:
            current_comment.delete()
            return HttpResponse('OK')
        return HttpResponseForbidden('You cannot delete this comment')
    except Discussion.DoesNotExist:
        return Http404('Discussion not found')
    except DiscussionComment.DoesNotExist:
        return Http404('comment not found')
