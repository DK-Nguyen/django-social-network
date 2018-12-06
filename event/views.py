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
    events = Event.objects.all()
    return render(request, 'event/event_list.html', {'events': events})


@login_required
def event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        participants = EventParticipant.objects.filter(event=event)
        find_user_participation = EventParticipant.objects.filter(event=event, invitee=request.user)
        is_participating = len(find_user_participation) > 0
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
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
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
    form = EventCreationForm()
    return render(request, 'event/event_new.html', {'form': form})


@login_required
@require_http_methods(['POST'])
def invite_participant(request, event_id, friend_id):
    event = Event.objects.get(id=event_id)
    inviter = request.user
    friend = SiteUser.objects.get(id=friend_id)
    find_participation_friend_invitee = EventParticipant.objects.filter(event=event, invitee=friend)
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
    try:
        event = Event.objects.get(id=event_id)
        invitee = EventParticipant.objects.get(event=event, invitee=request.user)
        if invitee.accepted:
            return HttpResponseBadRequest('You already accepted')
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
    try:
        event = Event.objects.get(id=event_id)
        invitee = EventParticipant.objects.get(event=event, invitee=request.user)
        invitee.delete()
        return redirect(event.get_absolute_url())
    except Event.DoesNotExist:
        return Http404('Event not found')
    except EventParticipant.DoesNotExist:
        return Http404('You are not invited')


@login_required
def event_edit(request, event_id):
    event_to_update = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventUpdateForm(request.POST, instance=event_to_update)
        if form.is_valid():
            edited_event = form.save()
            messages.success(request, 'Event has been updated')
            return redirect(edited_event.get_absolute_url())
        else:
            return render(request, 'event/event_edit.html', {'form': form})
    form = EventUpdateForm(instance=event_to_update)
    return render(request, 'event/event_edit.html', {'form': form})


@login_required
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        if event.owner != request.user:
            return HttpResponseForbidden('You are not the owner of this event')
        event.delete()
        return redirect('events')
    except Event.DoesNotExist:
        return Http404('Event does not exist')
