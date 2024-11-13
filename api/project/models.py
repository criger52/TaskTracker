from django.db import models

class Project(models.Model):
    projectURL = models.URLField(default='https://api/v1/user/project/')
    title = models.CharField(max_length=64)
    description = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=64, default='active')


