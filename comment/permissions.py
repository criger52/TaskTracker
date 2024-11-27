from comment.models import Comment
from rest_framework.permissions import BasePermission
from task.models import Task


class IsCreatorTask(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == Task.objects.get(id=request.data.get('task')).user.id

class IsCreatorComment(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == Comment.objects.get(id=view.kwargs.get('id')).user.id

# class IsRoleInProject(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.id
