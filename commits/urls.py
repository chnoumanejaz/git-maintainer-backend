from django.urls import path
from .views.github import save_github_credentials, get_github_credentials, remove_github_credentials, make_commits, get_commits_history
from .views.auth import register_user
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    # Auth endpoints
    path("register/", register_user, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),

    # GitHub API endpoints
    path("save_github/", save_github_credentials, name="save_or_update_github"),
    path("get_github/", get_github_credentials, name="get_github"),
    path("remove_github/", remove_github_credentials, name="remove_github"),
    path("make_commits/", make_commits, name="make_commits"),

    # Commit history endpoint
    path("history/", get_commits_history, name="commit_history"),
]