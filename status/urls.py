from django.urls import path
from . import views as discussion_view

urlpatterns = [
    path('discussions/', discussion_view.discussions, name='discussions'),

]
