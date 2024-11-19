from rest_framework import serializers

from .models import Project, Roles


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'date_of_creation', 'date_of_update', 'members']

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['name', 'id_user', 'id_project']




