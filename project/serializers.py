from rest_framework.serializers import ModelSerializer

from .models import Project, Roles


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'date_of_creation', 'creator', 'date_of_update']



class RolesSerializer(ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'name', 'id_user', 'id_project']

class AddRolesSerializer(ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'name', 'id_user']
        extra_kwargs = {
            'id_project': {'read_only': True},
        }

class ProjectListSerializers(ModelSerializer):
    roles = RolesSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'creator', 'roles']

class ProjectAllListSerializers(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'creator']


class ProjectCreateSerializer(ModelSerializer):
    role_in_proj = RolesSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'role_in_proj']
        extra_kwargs = {
            'creator': {'write_only': True},
        }


class ProjectMemberSerializer(ModelSerializer):
    roles = RolesSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'roles']


