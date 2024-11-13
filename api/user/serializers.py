from rest_framework import serializers


from .models import DefaultUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role_platform', 'avatar', 'projects', 'roles_in_project', 'pURL']