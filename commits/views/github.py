from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from commits.models import GitHubCredentials
from commits.serializers import GitHubCredentialsSerializer
import os, git, random, time
from github import Github
from datetime import datetime

# GitHub Credentials (Replace with your actual token)
# GITHUB_TOKEN = "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" # testing token
# GITHUB_USERNAME = "noumanejazz"

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

def push_commits(repo_name, num_commits, github_username, github_token):
    try:
        github = Github(github_token)
        user = github.get_user()
        repo = user.get_repo(repo_name)
        repo_url = repo.clone_url.replace("https://", f"https://{github_token}@")
        local_path = f"./{repo_name}"

        if not os.path.exists(local_path):
            git.Repo.clone_from(repo_url, local_path)

        repo = git.Repo(local_path)
        with repo.config_writer() as config:
            config.set_value("user", "name", github_username)
            config.set_value("user", "email", f"{github_username}@users.noreply.github.com")

        for _ in range(num_commits):
            problem = random.choice(CODE_SNIPPETS)
            filename = f"{problem['title']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{problem['file_type']}"
            file_path = os.path.join(local_path, filename)
            with open(file_path, "w") as f:
                f.write(problem["code"])

            repo.git.add(A=True)
            repo.index.commit(problem["commit_msg"])
            repo.remote().push()
            time.sleep(10)

        return {"status": "success", "message": "Commits pushed successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_github_credentials(request):
    """Save GitHub username and token"""
    print(request.user)
    serializer = GitHubCredentialsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "saved"})
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_github_credentials(request):
    """Get saved GitHub credentials"""
    credentials = GitHubCredentials.objects.first()
    if credentials:
        return Response(GitHubCredentialsSerializer(credentials).data)
    return Response({"error": "No credentials found"}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_github_credentials(request):
    """Remove GitHub credentials"""
    GitHubCredentials.objects.all().delete()
    return Response({"status": "removed"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_commits(request):
    """Make commits to GitHub repo"""
    credentials = GitHubCredentials.objects.first()
    if not credentials:
        return Response({"error": "GitHub credentials not found"}, status=400)

    repo_name = request.data.get("repo_name")
    num_commits = request.data.get("num_commits")

    if not repo_name or not num_commits:
        return Response({"error": "repo_name and num_commits are required"}, status=400)

    try:
        num_commits = int(num_commits)
    except ValueError:
        return Response({"error": "num_commits must be an integer"}, status=400)

    result = push_commits(repo_name, num_commits, credentials.github_username, credentials.github_token)
    return Response(result)
