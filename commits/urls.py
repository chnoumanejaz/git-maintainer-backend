from django.urls import path
from .views.github import save_github_credentials, get_github_credentials, remove_github_credentials, make_commits, get_commits_history
from .views.auth import register_user, login_user

urlpatterns = [
    # Auth endpoints
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
   #TODO: Add refresh token route

    # GitHub API endpoints
    path("save_github/", save_github_credentials, name="save_github"),
    path("get_github/", get_github_credentials, name="get_github"),
    path("remove_github/", remove_github_credentials, name="remove_github"),
    path("make_commits/", make_commits, name="make_commits"),

    # Commit history endpoint
    path("history/", get_commits_history, name="commit_history"),
]