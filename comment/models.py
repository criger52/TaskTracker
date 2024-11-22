import uuid

from django.db import models
from django.db.models import ForeignKey

from task.models import Task

from api import settings


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comment')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

