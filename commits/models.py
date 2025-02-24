from django.db import models
from django.contrib.auth.models import User

class CommitHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commit_history")
    #TODO: add the user_input field
    repo_name = models.CharField(max_length=255)
    num_commits = models.IntegerField()
    messages = models.JSONField(blank=True, null=True)
    is_pushed = models.BooleanField(default=False)
    new_repo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repo_name} - {self.num_commits} commits"

class GitHubCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="github_credentials")
    github_username = models.CharField(max_length=255, unique=True)
    github_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.github_username