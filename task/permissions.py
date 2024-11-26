
from project.models import Roles, Project
from rest_framework.permissions import BasePermission
from task.models import Task



class IsUserInProjectOrCreator(BasePermission):
    def has_permission(self, request, view):
        if view.kwargs.get('id') != None:
            try:
                task = Task.objects.get(id=view.kwargs.get('id'))
            except:
                return False
            # print(task.project.creator.id)
            if task.user.id == request.user.id or task.project.creator == request.user.id:
                return True
            return False
        try:
            roles = Roles.objects.filter(id_project=request.data.get('project'))
        except:
            return False
        flag = False
        for i in roles:
            if i.id_user.id == request.user.id:
                flag = True
                break
        try:
            Project.objects.get(id=request.data.get('project')).creator
        except:
            pass
        if flag or Project.objects.get(id=request.data.get('project')).creator.id == request.user.id:
            return True

class IsUserHaveTaskInProjectOrCreator(BasePermission):
    def has_permission(self, request, view):
        if (Task.objects.get(id=view.kwargs.get('id')).user == request.user) or request.user.id == Project.objects.get(id=request.data.get('project')).creator.id:
            return True
        return False