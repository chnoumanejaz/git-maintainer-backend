from django.urls import path
from .views import save_github_credentials, get_github_credentials, remove_github_credentials, make_commits

urlpatterns = [
    path("save_github/", save_github_credentials, name="save_github"),
    path("get_github/", get_github_credentials, name="get_github"),
    path("remove_github/", remove_github_credentials, name="remove_github"),
    path("make_commits/", make_commits, name="make_commits"),
]