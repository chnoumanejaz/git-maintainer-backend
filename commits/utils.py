import requests
from .constants import GITHUB_API_URL


def verify_github_credentials(username, token):
    """Check if GitHub credentials are valid"""
    response = requests.get(f"{GITHUB_API_URL}/user", auth=(username, token))
    return response.status_code == 200


