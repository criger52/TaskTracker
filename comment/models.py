from django.db import models
from django.db.models import ForeignKey

from task.models import Task

from api import settings


class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comment')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

