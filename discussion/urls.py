from django.conf.urls import url
from . import views as discussion_view

urlpatterns = [
    url(r'discussions/$', discussion_view.discussions, name='discussions'),
    url(r'discussions/new/$', discussion_view.new_discussion, name='new_discussion'),
    url(r'discussions/(\d{id})/$', discussion_view.discussion, name='discussion'),
]
