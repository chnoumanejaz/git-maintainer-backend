from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from commits.models import GitHubCredentials
from commits.serializers import GitHubCredentialsSerializer, GitHubCommitsSerializer
import os, git, time, json, re, shutil
from github import Github
from openai import OpenAI
from commits.openai.openai_models import OpenAIResponse


# GitHub Credentials (Replace with your actual token)
# GITHUB_TOKEN = "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" # testing token
# GITHUB_USERNAME = "noumanejazz"
API_KEY_DEEPSEEK = "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" # testing key


# Load system context from file
context_path = "commits/openai/context.txt"
print("context_path", context_path)

with open(context_path, "r") as file:
    system_context = file.read()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=API_KEY_DEEPSEEK,
)

def get_ai_response(user_input: str) -> OpenAIResponse:
    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_input}
        ]
    )

    response_text = completion.choices[0].message.content.strip()

    print("response_text", response_text , "\n\n\n\n\n\n\n\n\n")

    match = re.search(r'\{(.*)\}', response_text, re.DOTALL)
    extracted_response = ""
    if match:
        extracted_response = match.group(0)
        print(extracted_response)
    else:
        print("No data found inside {}")

    # Convert to a dictionary
    response_dict = json.loads(extracted_response)

    # Convert to Pydantic model
    return OpenAIResponse(**response_dict)


def push_commits(repo_name, num_commits, github_username, github_token, snippets):
    local_path = f"./{repo_name}"
    try:
        github = Github(github_token)
        user = github.get_user()
        new_repo = False

        # Check if repo exists, create if not
        try:
            repo = user.get_repo(repo_name)
        except Exception:
            print(f"⚠️ Repository '{repo_name}' not found. Creating a new repo...")
            repo = user.create_repo(repo_name, private=True)
            new_repo = True

        repo_url = repo.clone_url.replace("https://", f"https://{github_token}@")

        # Clone or pull the repo
        if os.path.exists(local_path):
            repo = git.Repo(local_path)
            repo.remote().pull()
        else:
            git.Repo.clone_from(repo_url, local_path)

        repo = git.Repo(local_path)

        # Set Git config
        with repo.config_writer() as config:
            config.set_value("user", "name", github_username)
            config.set_value("user", "email", f"{github_username}@users.noreply.github.com")

        # Create & push commits
        commit_messages = []
        for problem in snippets:
            filename = f"{problem.title}.{problem.file_type}"
            file_path = os.path.join(local_path, filename)

            with open(file_path, "w") as f:
                f.write(problem.code)

            repo.git.add(A=True)
            repo.index.commit(problem.commit_message)
            repo.remote().push()
            print(f"✅ Commit pushed: {problem.commit_message}")
            commit_messages.append(problem.commit_message)

            time.sleep(2)

        # Delete the cloned repository to free space
        shutil.rmtree(local_path, ignore_errors=True)
        return {"status": "success", "message": f"{num_commits} commits pushed successfully!", "messages": commit_messages, "new_repo": new_repo}

    except Exception as e:
        # Delete the cloned repository to free space
        shutil.rmtree(local_path, ignore_errors=True)
        return {"status": "error", "message": str(e), "messages": ["An error occurred while pushing the commits.", str(e)]}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_github_credentials(request):
    """Save GitHub username and token"""
    print(request.user)
    request.data["user"] = request.user.id
    serializer = GitHubCredentialsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"status": "Github credentials saved successfully!"})
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_github_credentials(request):
    """Get saved GitHub credentials"""
    try:
        credentials = GitHubCredentials.objects.get(user=request.user)
        return Response(GitHubCredentialsSerializer(credentials).data, status=200)

    except GitHubCredentials.DoesNotExist:
        return Response({"error": "No credentials found."}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_github_credentials(request):
    """Remove GitHub credentials"""
    try:
        credentials = GitHubCredentials.objects.get(user=request.user)
        credentials.delete()
        return Response({"status": "Github credentials removed successfully!"}, status=200)
    except GitHubCredentials.DoesNotExist:
        return Response({"error": "No credentials found."}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_commits(request):
    """Make commits to GitHub repo and save history"""
    credentials = GitHubCredentials.objects.filter(user=request.user).first()
    if not credentials:
        return Response({"error": "Please add the GitHub credentials first to make the commit"}, status=400)

    if not request.data.get("user_input"):
        return Response({"error": "Please provide a user input to make the commit"}, status=400)

    user_input = request.data.pop("user_input")

    # Save initial commit history
    request.data["user"] = request.user.id
    base_serializer = GitHubCommitsSerializer(data=request.data)
    if base_serializer.is_valid(raise_exception=True):
        commit_instance = base_serializer.save()

    repo_name = request.data["repo_name"]
    num_commits = request.data["num_commits"]

    result = None
    user_message = user_input + f" and make {num_commits} commits"
    response = get_ai_response(user_message)
    print("response--> ", response)

    if response and response.is_pushable:
        result = push_commits(repo_name, num_commits, credentials.github_username, credentials.github_token, response.snippets)
    else:
        result = {"status": "error", "messages": [response.response]}

    # Update commit history based on result
    update_data = {
        "messages": result.get("messages", [response.response]),
        "new_repo": result.pop("new_repo", False),
        "is_pushed": result["status"] == "success"
    }
    update_serializer = GitHubCommitsSerializer(commit_instance, data=update_data, partial=True)
    if update_serializer.is_valid(raise_exception=True):
        update_serializer.save()

    status_code = 201 if result["status"] == "success" else 400
    return Response(result, status=status_code)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_commits_history(request):
    """Get commit history of the user"""
    serializer = GitHubCommitsSerializer(request.user.commit_history, many=True)
    return Response(serializer.data, status=200)