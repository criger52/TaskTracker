from rest_framework import serializers

from .models import Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'password', 'role']