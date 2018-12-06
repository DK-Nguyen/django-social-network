from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, EventParticipant
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from users.models import SiteUser
from .forms import *


@login_required
def list_events(request):
    """
    This view show all events of the application for users, newest first. The Event model
    already specify ordering Meta so we don't have the order it here
    """
    events = Event.objects.all()
    return render(request, 'event/event_list.html', {'events': events})


@login_required
def event_details(request, event_id):
    """
    This view an event's detail about name, description, location, start and end date
    as well as participants (accepted or not). User can also search for their friend and
    invite them to event as well
    """
    try:
        event = Event.objects.get(id=event_id)
        participants = EventParticipant.objects.filter(event=event)

        # We are trying to see if user is invited to this event
        find_user_participation = EventParticipant.objects.filter(event=event, invitee=request.user)
        is_participating = len(find_user_participation) > 0

        # Finding out if current user is the one created this event
        is_owner = event.owner == request.user
        context = {
            'event': event,
            'participants': participants,
            'is_participating': is_participating,
            'accepted': is_participating and find_user_participation[0].accepted,
            'is_owner': is_owner
        }
        return render(request, 'event/event_details.html', context)
    except Event.DoesNotExist:
        return Http404('Event does not exist')


@login_required
def event_new(request):
    """
    This view show the UI for creating a new event
    """
    if request.method == 'POST':
        form = EventCreateAndUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_event = Event(
                owner=request.user,
                name=cleaned_data.get('name'),
                description=cleaned_data.get('description'),
                location=cleaned_data.get('location'),
                start_time=cleaned_data.get('start_time'),
                end_time=cleaned_data.get('end_time')
            )
            new_event.save()
            messages.success(request, 'Event has been created')
            return redirect(new_event.get_absolute_url())
        return render(request, 'event/event_new.html', {'form': form})
    form = EventCreateAndUpdateForm()
    return render(request, 'event/event_new.html', {'form': form})


@login_required
@require_http_methods(['POST'])
def invite_participant(request, event_id, friend_id):
    """
    This view handles request to add a friend to an event
    :param event_id: id of the event
    :param friend_id: user id of the friend
    """
    event = Event.objects.get(id=event_id)
    inviter = request.user
    friend = SiteUser.objects.get(id=friend_id)

    # Find out if this friend is already invited
    find_participation_friend_invitee = EventParticipant.objects.filter(event=event, invitee=friend)

    # Find out if the inviter is already participating the event or the event owner
    find_participation_inviter = EventParticipant.objects.filter(event=event, invitee=inviter, accepted=True)
    if len(find_participation_inviter) == 0 and event.owner != inviter:
        return HttpResponseForbidden('You are not a participant of this')

    if len(find_participation_friend_invitee) == 0:
        new_participant = EventParticipant(event=event, inviter=inviter, invitee=friend)
        new_participant.save()
        messages.success(request, 'Invited friend')
        return redirect(event.get_absolute_url())
    return HttpResponseBadRequest('Friend is already invited')


@login_required
@require_http_methods(['POST'])
def accept_participation(request, event_id):
    """
    As the user if they want to accept an invitation to an event they will request to this
    view
    """
    try:
        event = Event.objects.get(id=event_id)
        invitee = EventParticipant.objects.get(event=event, invitee=request.user)
        if invitee.accepted:
            return HttpResponseBadRequest('You already accepted')
        messages.success(request, 'Yay! You are now officially in this event!')
        invitee.accepted = True
        invitee.save()
        return redirect(event.get_absolute_url())
    except Event.DoesNotExist:
        return Http404('Event not found')
    except EventParticipant.DoesNotExist:
        return Http404('You are not invited')


@login_required
@require_http_methods(['POST'])
def leave_or_reject_event(request, event_id):
    """
    If user want to reject or leave an event, they will request this view. Since a participation
    is saved as a Model so deleting that both means leaving or rejecting
    :return:
    """
    try:
        event = Event.objects.get(id=event_id)
        invitee = EventParticipant.objects.get(event=event, invitee=request.user)
        invitee.delete()
        messages.success(request, 'You have been out of this event!')
        return redirect(event.get_absolute_url())
    except Event.DoesNotExist:
        return Http404('Event not found')
    except EventParticipant.DoesNotExist:
        return Http404('You are not invited')


@login_required
def event_edit(request, event_id):
    """
    This view render UI to edit an event
    """
    event_to_update = Event.objects.get(id=event_id)
    if request.user != event_to_update.owner:
        return HttpResponseForbidden('You are not the owner of this event!')
    if request.method == 'POST':
        form = EventCreateAndUpdateForm(request.POST, instance=event_to_update)
        if form.is_valid():
            edited_event = form.save()
            messages.success(request, 'Event has been updated')
            return redirect(edited_event.get_absolute_url())
        else:
            return render(request, 'event/event_edit.html', {'form': form})
    form = EventCreateAndUpdateForm(instance=event_to_update)
    return render(request, 'event/event_edit.html', {'form': form})


@login_required
def delete_event(request, event_id):
    """
    The owner of an event can delete the event by requesting this link
    """
    try:
        event = Event.objects.get(id=event_id)

        # All participation needs to be deleted as well
        participants = EventParticipant.objects.filter(event=event)
        for participant in participants:
            participant.delete()

        if event.owner != request.user:
            return HttpResponseForbidden('You are not the owner of this event')
        event.delete()
        return redirect('events')
    except Event.DoesNotExist:
        return Http404('Event does not exist')
