from django.urls import path
from . import views as event_views

urlpatterns = [
    path('events/', event_views.list_events, name='events'),
    path('events/new/', event_views.event_new, name='new_event'),
    path('events/<int:event_id>/', event_views.event_details, name='event_details'),
]
