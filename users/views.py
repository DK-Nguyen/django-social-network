from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import SiteUser
from friends.models import FriendRequest
from friends.views import send_friend_request, accept_friend_request


def home(request):
    return render(request, 'users/home.html')


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


def register(request):
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
def profile(request):
    # p = request.user
    # id_to_exclude = [i.id for i in request.user.friends.id]
    other_users = SiteUser.objects.exclude(id=request.user.id)
    friends = request.user.friends.all()
    frequest = FriendRequest.objects.all()

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
    }

    return render(request, 'users/profile.html', context)


def other_profile(request, pk=None):
    if pk:
        user = SiteUser.objects.get(pk=pk)
    else:
        user = request.user
    context = {'user': user}
    return render(request, 'users/other_profiles.html', context)


@login_required
def friends_profile(request, pk=None):
    if pk:
        friend = SiteUser.objects.get(pk=pk)
    else:
        friend = request.user

    context = {'user': friend}

    return render(request, 'users/friend_profile.html', context)


@login_required
def change_info(request):
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

