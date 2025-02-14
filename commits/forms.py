from django import forms

class CommitForm(forms.Form):
    repo_name = forms.CharField(label="GitHub Repository Name", max_length=255)
    num_commits = forms.IntegerField(label="Number of Commits")