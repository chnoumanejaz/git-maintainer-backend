from rest_framework import serializers
from .models import GitHubCredentials

class GitHubCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubCredentials
        fields = '__all__'