from django.shortcuts import render, redirect
from .models import Status, StatusComment
from .forms import StatusCreationForm, StatusCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods


@login_required
def status_comments(request, status_id):
    """
    This function creates a form for the user to comment on a status

    :param
        status_id: the id of the status to comment on

    """
    try:
        current_status = Status.objects.get(id=status_id)
        comments = StatusComment.objects.filter(status=current_status)
        comment_list = [i for i in comments]
        owner = current_status.owner

        if request.method == 'POST':
            comment_form = StatusCommentForm(request.POST)
            # POST submits data to be processed (e.g., from an HTML form) to the identified resource.
            # The data is included in the body of the request.
            # This may result in the creation of a new resource or the updates of existing resources or both.
            if comment_form.is_valid():
                cleaned_data = comment_form.cleaned_data
                new_status_comment = StatusComment(
                    content=cleaned_data.get('content'),
                    status=current_status,
                    commenter=request.user,
                )
                new_status_comment.save()
                messages.success(request, 'Comment has been created')
                return redirect(current_status.get_absolute_url())
        else:

            comment_form = StatusCommentForm()

        context = {
            'status': current_status,
            'comments': comment_list,
            'owner': owner,
            'comment_form': comment_form,
            'user': request.user
        }
    except Status.DoesNotExist:
        return Http404('Discussion not found')

    return render(request, 'status/status_comments.html', context)


@login_required
def delete_status(request, status_id):
    """
    This function deletes a status with the id specified in the parameter "status_id"

    :param status_id: the id of the status to be deleted
    """

    current_status = Status.objects.get(id=status_id)
    try:
        comments = StatusComment.objects.filter(status=current_status)
        comment_list = [i for i in comments]
        if request.user == current_status.owner:
            current_status.delete()
            for comment in comment_list:
                comment.delete()
            return redirect("profile")
        redirect('profile')
        return HttpResponseForbidden('You cannot delete this comment')
    except Status.DoesNotExist:
        return Http404('Status not found')
