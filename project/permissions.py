from project.models import Project, Roles
from rest_framework.permissions import BasePermission


class IsCreatorOrTeamLead(BasePermission):
    def has_permission(self, request, view):
        try:
            role = Roles.objects.get(id_user=request.user.id, id_project=view.kwargs.get('id'))
        except Roles.DoesNotExist:
            if Project.objects.get(id=view.kwargs.get('id')).creator == request.user:
                return True
            return False
        if (Project.objects.get(id=view.kwargs.get('id')).creator == request.user) or (str(Roles.objects.get(id_user=request.user.id, id_project=view.kwargs.get('id'))) == 'TeamLead'):
            return True
        return False