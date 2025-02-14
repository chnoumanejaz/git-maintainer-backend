from django.urls import path
from .views import commit_view

urlpatterns = [
    path("", commit_view, name="commit_view"),
]