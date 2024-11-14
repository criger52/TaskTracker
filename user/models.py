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
    avatar = models.ImageField(upload_to='avatar/', default='avatar/def.jpg', blank=True, null=True)
    # projects = models.ManyToManyField(Project, blank=True)
    # roles_in_project = models.JSONField(blank=True, default=dict, null=True)
    # при удалении user`а надо удалять все соданные им проекты


