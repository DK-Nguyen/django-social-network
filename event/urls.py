from django.urls import path
from . import views as event_views

urlpatterns = [
    path('events/', event_views.list_events, name='events'),
    path('events/new/', event_views.event_new, name='new_event'),
    path('events/<int:event_id>/', event_views.event_details, name='event_details'),
    path('events/<int:event_id>/edit', event_views.event_edit, name='edit_event'),
    path('events/<int:event_id>/invite/<int:friend_id>/', event_views.invite_participant, name='invite_participant'),
    path('events/<int:event_id>/accept_invite/', event_views.accept_participation, name='accept_invitation'),
    path('events/<int:event_id>/leave', event_views.leave_or_reject_event, name='leave_or_reject_event'),
    path('events/<int:event_id>/delete', event_views.delete_event, name='delete_event')
]
