from rest_framework.serializers import ModelSerializer

from .models import Task
from comment.seializers import CommentSerializer


class TaskSerializer(ModelSerializer):
    comment = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'user', 'status', 'priority', 'create_date', 'last_update_date', 'deadline', 'tester', 'comment']

class TaskInProjectSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description','user', 'status', 'priority','deadline', 'tester']

class TaskCreate(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user', 'project', 'status', 'priority', 'deadline', 'tester']



