from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required
def list_events(request):
    return render(request, 'event/event_list.html', {'events': []})


@login_required
def event_details(request):
    return render(request, 'event/event_details.html')


@login_required
def event_new(request):
    if request.method == 'POST':
        pass
    form = EventCreationForm()
    return render(request, 'event/event_new.html', {'form': form})

