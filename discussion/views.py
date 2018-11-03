from django.shortcuts import render, redirect


def discussions(request):
    return render(request, 'discussions.html')


def new_discussion(request):
    return render(request, 'new_discussion.html')


def discussion(request):
    return render(request, 'discussion.html')
