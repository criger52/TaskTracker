from rest_framework import serializers


from .models import DefaultUser
from project.serializers import ProjectSerializer



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)
    created_projects = ProjectSerializer(many=True, read_only=True)  # Вложенный сериализатор
    class Meta:
        model = DefaultUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'role_platform', 'avatar', 'created_projects']