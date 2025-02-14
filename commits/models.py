from django.db import models

class CommitHistory(models.Model):
    repo_name = models.CharField(max_length=255)
    num_commits = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repo_name} - {self.num_commits} commits"


class GitHubCredentials(models.Model):
    github_username = models.CharField(max_length=255, unique=True)
    github_token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.github_username