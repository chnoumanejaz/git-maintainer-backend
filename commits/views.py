from django.shortcuts import render
from .forms import CommitForm
import os
import git
import random
import time
from github import Github
from datetime import datetime

# GitHub Credentials (Replace with your actual token)
GITHUB_TOKEN = "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" # testing token
GITHUB_USERNAME = "noumanejazz"

# Code snippets for commits
CODE_SNIPPETS = [
    {
        "title": "two_sum",
        "commit_msg": "Added optimized Python solution for Two Sum problem",
        "file_type": "py",
        "code": '''# LeetCode Problem: Two Sum
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
'''
    }
]

def push_commits(repo_name, num_commits):
    try:
        github = Github(GITHUB_TOKEN)
        user = github.get_user()
        repo = user.get_repo(repo_name)
        repo_url = repo.clone_url.replace("https://", f"https://{GITHUB_TOKEN}@")
        local_path = f"./{repo_name}"

        if not os.path.exists(local_path):
            git.Repo.clone_from(repo_url, local_path)

        repo = git.Repo(local_path)

        with repo.config_writer() as config:
            config.set_value("user", "name", GITHUB_USERNAME)
            config.set_value("user", "email", f"{GITHUB_USERNAME}@users.noreply.github.com")

        for i in range(num_commits):
            problem = random.choice(CODE_SNIPPETS)
            commit_message = problem["commit_msg"]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{problem['title']}_{timestamp}.{problem['file_type']}"
            file_path = os.path.join(local_path, filename)

            with open(file_path, "w") as f:
                f.write(problem["code"])

            repo.git.add(A=True)
            repo.index.commit(commit_message)
            repo.remote().push()
            time.sleep(10)

        return "Commits pushed successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def commit_view(request):
    message = ""
    if request.method == "POST":
        form = CommitForm(request.POST)
        if form.is_valid():
            repo_name = form.cleaned_data["repo_name"]
            num_commits = form.cleaned_data["num_commits"]
            message = push_commits(repo_name, num_commits)
    else:
        form = CommitForm()

    return render(request, "commits/index.html", {"form": form, "message": message})
