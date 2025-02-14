from rest_framework import serializers
from .models import GitHubCredentials
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class GitHubCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubCredentials
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return {'user': user}
