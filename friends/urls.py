from django.urls import path
from friends import views as friends_views

urlpatterns = [
    path('friend-request/send/<int:id>/', friends_views.send_friend_request, name='send_request'),
    path('friend-request/cancel/<int:id>/', friends_views.cancel_friend_request, name='cancel_request'),
    path('friend-request/accept/<int:id>/', friends_views.accept_friend_request, name='accept_request'),
    path('friend-request/delete/<int:id>/', friends_views.delete_friend_request, name='delete_request'),
    path('search', friends_views.search_friend, name="search_friend"),
]
