from rest_framework import serializers

from .models import Project, Roles
from task.serializers import TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'date_of_creation', 'date_of_update', 'members', 'tasks']

class ProjectTitleIDSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['name', 'id_user', 'id_project']




