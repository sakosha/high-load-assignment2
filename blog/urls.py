from django.urls import path

from .views import PostListView
from .views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('posts/', PostListView.as_view(), name='posts'),
]
