from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import SiteUser
from friends.models import FriendRequest
from status.models import Status
from status.forms import StatusCreationForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


@login_required
def modify_base(request):
    """
    This function is used to give the base.html the information about the user that sends
    a http request.
    """
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'base.html', context)


def register(request):
    """
    This function is used to create a form for a new user to register
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can log in now!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def change_info(request):
    """
    This function is used to create a form for a user to update his information
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/change_info.html', context)


@login_required
def profile(request):
    """
    This function is used to query the data for a user that already logged in to show them to the profile page.

    """
    # p = request.user
    # id_to_exclude = [i.id for i in request.user.friends.id]
    other_users = SiteUser.objects.exclude(id=request.user.id)
    friends = request.user.friends.all()
    frequest = FriendRequest.objects.all()
    statuses = Status.objects.filter(owner_id=request.user.id)
    status_list = []
    for status in statuses:
        status_list.append(status)

    if request.method == 'POST':
        status_form = StatusCreationForm(request.POST)
        if status_form.is_valid():
            cleaned_data = status_form.cleaned_data
            new_status = Status(
                content=cleaned_data.get('content'),
                owner=request.user
            )
            new_status.save()
            messages.success(request, 'Status has been created')
            return redirect('profile')
    else:
        status_form = StatusCreationForm()

    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    received_friend_requests = FriendRequest.objects.filter(to_user=request.user)

    sent_to_ids = []
    for friend_request in sent_friend_requests:
        sent_to_ids.append(friend_request.get_to_user_id())

    received_from_ids = []
    for friend_request in received_friend_requests:
        received_from_ids.append(friend_request.get_from_user_id())

    context = {
        'other_users': other_users,
        'friends': friends,
        'frequest': frequest,
        'sent_to_ids': sent_to_ids,
        'received_from_ids': received_from_ids,
        'statuses': status_list,
        'status_form': status_form,
    }

    return render(request, 'users/profile.html', context)


def other_profile(request, id=None):
    """
    This function is used to get the data of a user who are not friends of the user that sends the http request.

    :param
        id: the id of the user whose profile page is to be seen
    """
    if id:
        other_user = SiteUser.objects.get(id=id)
    else:
        other_user = request.user
    context = {'other_user': other_user}
    return render(request, 'users/other_profiles.html', context)


@login_required
def friends_profile(request, id=None):
    """
    This function is used to get the data of a friend of the user who sends the http request.

    :param
        id: the id of the friend

    """
    if id:
        friend = SiteUser.objects.get(id=id)
        statuses = Status.objects.filter(owner_id=id)
        status_list = []
        for status in statuses:
            status_list.append(status)
    else:
        friend = request.user

    context = {
        'friend': friend,
        'statuses': status_list,
    }

    return render(request, 'users/friend_profile.html', context)


