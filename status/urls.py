from django.urls import path
from . import views as status_view

urlpatterns = [
    path('<int:status_id>/', status_view.status_comments, name='status_comments'),
    path('delete/<int:status_id>/', status_view.delete_status, name='delete_status'),
]
