from django.db import models
from rest_framework.fields import URLField

from project.models import Project
from user.models import DefaultUser


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')  # поменять на uuid
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)  # поменять на uuid

    STATUS_CHOICES = (
        ('Grooming', 'Grooming'),
        ('In progress', 'In progress'),
        ('Dev', 'Dev'),
        ('Done', 'Done')
    )

    PRIORITY_CHOICES = (
        ('Low', 'Низкий'),
        ('Medium', 'Средний'),
        ('High', 'Высокий'),
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, default='Medium')
    create_date = models.DateField(auto_now_add=True)
    last_update_date = models.DateField(auto_now=True)
    deadline = models.DateField()
    responsible_fot_test = models.ForeignKey(DefaultUser, on_delete=models.CASCADE, related_name='responsible')



    def __str__(self):
        return self.title