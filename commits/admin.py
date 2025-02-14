from django.contrib import admin
from commits.models import *

models = [CommitHistory, GitHubCredentials]

for model in models:
    admin.site.register(model)