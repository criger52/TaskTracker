import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from project.models import Project


class DefaultUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=123, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    role_platform = models.CharField(max_length=255, default='Beginner')
    avatar = models.ImageField()
    projects = models.ManyToManyField(Project, blank=True, null=True)
    roles_in_project = models.JSONField(blank=True, default=dict)

    @property
    def pURL(self):
        return f'https://api/v1/user/projects/{self.id}/'

