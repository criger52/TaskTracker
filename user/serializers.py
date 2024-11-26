from project.serializers import ProjectSerializer, RolesSerializer
from rest_framework import serializers

from .models import DefaultUser


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)
    role_in_proj = RolesSerializer(many=True, read_only=True)

    class Meta:
        model = DefaultUser
        fields = ['id', 'username', 'first_name', 'last_name', 'role_platform', 'avatar', 'history_project', 'role_in_proj']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

class UserProfileForAllSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)
    role_in_proj = RolesSerializer(many=True, read_only=True)
    class Meta:
        model = DefaultUser
        fields = ['username', 'first_name', 'last_name', 'role_platform', 'avatar', 'role_in_proj', 'history_project']





class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'role_platform']

    def create(self, validated_data):
        user = DefaultUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role_platform=validated_data['role_platform'],
        )
        return user

class UserProjectSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    role_in_proj = RolesSerializer(many=True, read_only=True)
    class Meta:
        model = DefaultUser
        fields = ['projects', 'role_in_proj']