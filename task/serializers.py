from rest_framework import serializers

from .models import Task
from comment.seializers import CommentSerializer


class TaskSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'user', 'status', 'priority', 'create_date', 'last_update_date', 'deadline', 'responsible_fot_test', 'comment']