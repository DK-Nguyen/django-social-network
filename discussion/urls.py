from django.urls import path
from . import views as discussion_view

urlpatterns = [
    path('', discussion_view.discussions, name='discussions'),
    path('new/', discussion_view.new_discussion, name='new_discussion'),
    path('<int:discussion_id>/', discussion_view.discussion, name='discussion'),
    path('<int:discussion_id>/edit/', discussion_view.edit_discussion, name='edit_discussion'),
    path('<int:discussion_id>/comments/new', discussion_view.post_comments, name='new_comment'),
    path('<int:discussion_id>/comments/', discussion_view.get_comments, name='fetch_comments'),
    path('<int:discussion_id>/comments/<int:comment_id>/', discussion_view.delete_comment, name="delete_comments"),
    path('<int:discussion_id>/participants/new/<int:friend_id>/', discussion_view.invite_participant, name="invite_participant"),
    path('<int:discussion_id>/leave', discussion_view.leave_discussion, name="leave_discussion"),
]
