from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('', users_views.profile, name='profile'),
    path('home', users_views.home, name='home'),
    path('register/', users_views.register, name='register'),
    path('about/', users_views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', users_views.profile, name='profile'),
    path('profile/changeInfo/', users_views.change_info, name='change_info'),
    path('profile/<int:pk>/', users_views.other_profile, name='profile_with_pk'),
    # url(r'^profile/(?P<pk>\d+)/$', users_views.profile, name='profile_with_pk'),
    path('profile/friends/<int:pk>/', users_views.friends_profile, name='friend_profile'),
]

