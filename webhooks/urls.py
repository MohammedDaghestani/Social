from django.urls import path
from .views import (
    TestView,
    # GetWebhooks,
    )
app_name = 'webhooks'
urlpatterns = [
    path('', TestView.as_view()),
]