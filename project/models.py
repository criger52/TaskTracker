import uuid

from django.conf import settings
from django.db import models

class Project(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=64, default='active')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')

    def __str__(self):
        return self.title






