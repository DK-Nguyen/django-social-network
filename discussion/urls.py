from django.urls import path
from . import views as discussion_view

urlpatterns = [
    path('discussions/', discussion_view.discussions, name='discussions'),
    path('discussions/new/', discussion_view.new_discussion, name='new_discussion'),
    path('discussions/<int:discussion_id>/', discussion_view.discussion, name='discussion'),
]
