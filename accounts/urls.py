from accounts.forms import RegisterForm
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    RegisterView,
    ProfileView,
    FacebookLoginView,
    RemoveProfileView,
)

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name= 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('facebook-login/', FacebookLoginView.as_view(), name='facebook-login'),
    path('remove-profile/', RemoveProfileView.as_view(), name='remove-profile'),    
]
