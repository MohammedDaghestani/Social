from accounts.forms import RegisterForm
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    RegisterView,
    DashboardView,
    FacebookLoginView,
    FacebookProfileView,
    AddPost,
    AutomatePostCommentsResponseView,
    FacebookMorePosts,
    FacebookSearchPostsView,
    FacebookScheduledPostsView,
    FacebookLifeTimePostsView,
    FacebookPublishedPostsView,
    ReplyView,
)

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name= 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('facebook-login/', FacebookLoginView.as_view(), name='facebook-login'),
    path('facebook/posts', FacebookProfileView.as_view(), name='facebook-profile'),
    path('facebook/more-posts', FacebookMorePosts.as_view(), name='facebook-more-posts'),
    path('facebook/scheduled-posts', FacebookScheduledPostsView.as_view(), name='facebook-scheduled-posts'),
    path('facebook/published-posts', FacebookPublishedPostsView.as_view(), name='facebook-published-posts'),
    path('facebook/posts/<str:lifetime>', FacebookLifeTimePostsView.as_view(), name = 'facebook-posts-lifetime'),
    path('add-post/', AddPost.as_view(), name='add-post'),
    path('add-automate-response/<str:post_id>/', AutomatePostCommentsResponseView.as_view(), name='response'),
    path('facebook/search-post/<str:post_id>', FacebookSearchPostsView.as_view() ,name='search-post'),
    path('facebook/post/reply', ReplyView.as_view(), name='reply'),
]
