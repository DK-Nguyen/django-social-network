from django.urls import path
from . import views as discussion_view

urlpatterns = [
    path('discussions/', discussion_view.discussions, name='discussions'),
    path('discussions/new/', discussion_view.new_discussion, name='new_discussion'),
    path('discussions/<int:discussion_id>/', discussion_view.discussion, name='discussion'),
    path('discussions/<int:discussion_id>/edit/', discussion_view.edit_discussion, name='edit_discussion'),
    path('discussions/<int:discussion_id>/comments/new', discussion_view.post_comments, name='new_comment'),
    path('discussions/<int:discussion_id>/comments/', discussion_view.get_comments, name='fetch_comments'),
    path('discussions/<int:discussion_id>/comments/<int:comment_id>/', discussion_view.delete_comment, name="delete_comments")
]
