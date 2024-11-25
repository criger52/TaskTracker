import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models



class DefaultUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=123, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    role_platform = models.CharField(max_length=255, default='Beginner')
    avatar = models.ImageField(upload_to='avatar/', default='avatar/def.jpg', blank=True, null=True)
    history_project = models.TextField(blank=True)

    def __str__(self):
        return self.username


