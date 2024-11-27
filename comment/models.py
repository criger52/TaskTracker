import uuid

from django.db import models
from django.db.models import ForeignKey
from task.models import Task

from api.settings import AUTH_USER_MODEL


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comment')
    user = ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('text', 'task')

    def __str__(self):
        return f'comment {self.id}'

