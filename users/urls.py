from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, CustomLoginView, UserListView, ban_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('creators/', UserListView.as_view(), name='creators'),
    path('ban-user/<int:pk>/', ban_user, name='ban_user'),
]