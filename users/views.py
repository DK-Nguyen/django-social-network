from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import SiteUser

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
    users = SiteUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'users/profile.html', context)


def other_profile(request, pk=None):
    if pk:
        user = SiteUser.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'users/other_profiles.html', args)


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
