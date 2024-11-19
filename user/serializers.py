from rest_framework import serializers


from .models import DefaultUser
from project.serializers import ProjectSerializer, RolesSerializer


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)
    projects = ProjectSerializer(many=True, read_only=True)
    role_in_proj = RolesSerializer(many=True, read_only=True)

    class Meta:
        model = DefaultUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'role_platform', 'avatar', 'projects', 'history_project', 'role_in_proj']


