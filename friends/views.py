from friends.models import FriendRequest
from users.models import SiteUser
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from gravatar.tags import gravatar_url


@login_required
def send_friend_request(request, id):
    """
    This function creates a FriendRequest object from the user that sent the request
    to the user with the id specified in the parameter "id"

    :param id:
        the id of the user that the request will be sent to
    """

    try:
        to_user = SiteUser.objects.get(id=id)
        frequest, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        return redirect('profile')

    except:
        HttpResponseBadRequest('Bad request')


@login_required
def cancel_friend_request(request, id):
    """
    This function deletes the FriendRequest object from the user that sent the http request
    to the user with the id specified in the parameter "id"

    :param id:
        the id of the user that the request will be sent to
    """
    try:
        to_user = SiteUser.objects.get(id=id)
        frequest = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).first()
        frequest.delete()
        return redirect('profile')
    except:
        HttpResponseBadRequest('Bad request')


@login_required
def accept_friend_request(request, id):
    """
    This function checks the friend request from the user with the id specified in the
    parameter "id" to the user that sent the http request, then connect them by adding
    each other to other's friend list.

    :param id:
        the id of the user that sent the request
    """
    try:
        from_user = SiteUser.objects.get(id=id)
        frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
        u1 = frequest.to_user
        u2 = from_user
        u1.friends.add(u2)
        u2.friends.add(u1)
        frequest.delete()
        return redirect('profile')
    except:
        HttpResponseBadRequest('Bad request')


@login_required
def delete_friend_request(request, id):
    """
    This function checks the friend request from the user with the id specified in the
    parameter "id" to the user that sent the http request, then delete that friend request

    :param id:
        the id of the user that sent the request
    """
    try:
        from_user = SiteUser.objects.get(id=id)
        frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
        frequest.delete()
        return redirect('profile')
    except:
        HttpResponseBadRequest('Bad request')


@login_required
@require_http_methods(["GET"])
def search_friend(request):
    """
    This function is used to find the friend with the name specified in 'query'

    :return:
        The list of friends with match name.
    """
    query = request.GET.get('query')
    if len(query) < 1:
        return HttpResponseBadRequest('Search query too short')
    search_friends = request.user.friends.filter(first_name__istartswith=query)[:10]
    response = []
    for friend in search_friends:
        response.append({
            'name': friend.name(),
            'profile_picture': gravatar_url(friend.email, 30),
            'id': friend.id
        })
    return JsonResponse({'data': response})


@login_required
# @require_http_methods(["DELETE"])
def delete_friend(request, id):
    """
    This function is used to delete a friend of a user that sends the http request
    :param id: the id of the friend to be deleted
    """
    try:
        user = request.user
        to_be_deleted_friend = user.friends.filter(id=id).first()
        user.friends.remove(to_be_deleted_friend)
        to_be_deleted_friend.friends.remove(user)
        return redirect('profile')
    except:
        HttpResponseBadRequest('Bad request')