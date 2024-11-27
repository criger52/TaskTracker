import uuid

from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('archive', 'archive'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(default='')
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES,default='active')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'creator')


    def __str__(self):
        return self.title


class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='role_in_proj')
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles')

    class Meta:
        unique_together = ('id_user', 'id_project')

    def __str__(self):
        return self.name



















