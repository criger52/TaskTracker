from django.db.models import JSONField
from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'date_of_creation', 'date_of_update', 'created_by', 'members']