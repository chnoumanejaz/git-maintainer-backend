from django.db import models

class CommitHistory(models.Model):
    repo_name = models.CharField(max_length=255)
    num_commits = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repo_name} - {self.num_commits} commits"