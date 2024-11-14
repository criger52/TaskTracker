from tkinter.constants import CASCADE

from django.conf import settings
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=64, default='active')
    # members = models.JSONField(default={"creator": "URL"})
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')

    def __str__(self):
        return self.title






