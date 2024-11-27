from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from task.models import Task
from task.serializers import TaskInProjectSerializer
from user.models import DefaultUser

from .permissions import IsCreatorOrTeamLead
from .serializers import *


@extend_schema(
        summary="Создает новый проект",
        description="Создает новый проект, доступен для аутентифицированных",
        request=ProjectCreateSerializer,
    )
class ProjectCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


@extend_schema(
        summary="Получает список всех проектов",
        description="Получает список всех проектов, доступен для всех(есть сортировка)",
        request=ProjectAllListSerializers,
    )
class ProjectAll(APIView):
    permission_classes = (AllowAny, )
    queryset = Project.objects.all()
    serializer_class = ProjectAllListSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["date_of_creation", "date_of_update", "title"]
    ordering = ["date_of_creation"]

    def get(self, request, *args, **kwargs):
        order_by = request.data.get('order_by', None)
        projects = Project.objects.all()
        if order_by:
            valid_ordering = []
            for i in order_by.split(','):
                if i in self.ordering_fields:
                    valid_ordering.append(i)
            if valid_ordering:
                projects = projects.order_by(*valid_ordering)
        serializer = self.serializer_class(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
        summary="Получение конкретного проекта по id",
        description="Получение конкретного проекта по id, доступен для всех",
        request=ProjectListSerializers,
    )
class ProjectByUUID(RetrieveAPIView):
    permission_classes = (AllowAny, )
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    lookup_field = 'id'

@extend_schema(
        summary="Изменение/удаление конкретного проекта по id",
        description="Изменение/удаление конкретного проекта по id, доступен для создателей проекта или для участников с ролью TeamLead",
        request=ProjectListSerializers,
        responses={
            200: OpenApiResponse(response=ProjectListSerializers, description="Проект успешно изменен"),
            400: OpenApiResponse( description="Ошибка валидации"),
            204: OpenApiResponse(description="Проект успешно удален")
        }
    )
class ProjectEdit(GenericAPIView):
    permission_classes = (IsCreatorOrTeamLead, )  # IsOwner
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    lookup_field = 'id'

    def patch(self, request , *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        serializer = self.get_serializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "project is updated"}, status=status.HTTP_200_OK)
        return Response({"detail": "not valid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@extend_schema(
        summary="Получение ролей в конкретном проекте",
        description="Получение ролей в конкретном проекте, доступен для всех",
        request=ProjectMemberSerializer,
    )
class ProjectListMembers(APIView):
    permission_classes = (AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectMemberSerializer

    def get(self, request, *args, **kwargs):
        id_project = kwargs.get('id')
        roles = Roles.objects.filter(id_project=id_project)
        serializer = RolesSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllRoles(ListAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

@extend_schema(
        summary="Создание новой роли в проекте",
        description="создание новой роли в проекте, доступен для создателей проекта или для участников с ролью TeamLead",
        request=AddRolesSerializer,
        responses={
            200: OpenApiResponse(response=AddRolesSerializer, description="Роль успешно создана"),
            400: OpenApiResponse( description="Ошибка валидации"),
        }
    )
class AddRole(APIView):
    permission_classes = (IsCreatorOrTeamLead, )
    queryset = Roles.objects.all()
    serializer_class = AddRolesSerializer

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(id_project=project)
            user = DefaultUser.objects.get(id=request.data.get('id_user'))
            ls = user.history_project.split()
            if project.title not in ls:
                ls.append(project.title)
            user.history_project = ' '.join(ls)
            user.save()
            try:
                send_mail('Вас добавили в проект',
                          f'Вас добавили в проект {project.title}',
                          'vladimirv2312@gmail.com',
                        ['kirillchernovinsky@yandex.ru'])
            except:
                pass
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notifications",
                    {
                        "type": "send_notification",
                        "message": {
                            "title": "Новое уведомление",
                            "body": f"Вас добавили в проект {project.title}",
                            "project_id": project.id,
                        },
                    },
                )
            except:
                pass

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        summary="Изменение/удаление роли в проекте",
        description="Изменение/удаление роли в проекте, доступен для создателей проекта или для участников с ролью TeamLead",
        request=RolesSerializer,
        responses={
            200: OpenApiResponse(response=AddRolesSerializer, description="Роль успешно обновлена"),
            400: OpenApiResponse(description="Ошибка валидации"),
            204: OpenApiResponse(description="Роль успешно удалена")
        }
    )
class ProjectMemberEdit(APIView):
    permission_classes = (IsCreatorOrTeamLead,)
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        role = Roles.objects.get(id=kwargs['id_role'])
        serializer= self.serializer_class(role, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        role = Roles.objects.get(id=kwargs['id_role'])
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
        summary="Получение заданий конкретного проекта",
        description="Получение задания конкретного проекта, доступен для всех",
        request=TaskInProjectSerializer,
        responses={
            200: OpenApiResponse(response=TaskInProjectSerializer, description="Задачи успешно получены"),
        }
    )
class TaskProject(APIView):
    permission_classes = (AllowAny,)
    queryset = Task.objects.all()
    serializer_class = TaskInProjectSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get('id_task',None):
            task = Task.objects.get(id=kwargs.get('id_task',None))
            serializer = self.serializer_class(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        tasks = Task.objects.filter(project=kwargs.get('id'))
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class TaskProjectEdit(APIView):
#     permission_classes = (IsAdminUser,)
#     queryset = Task.objects.all()
#     serializer_class = TaskInProjectSerializer
#
#     def patch(self, request, *args, **kwargs):
#         task = Task.objects.get(id=kwargs['id_task'])
#         serializer = self.serializer_class(task, request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         task = Task.objects.get(id=kwargs['id_task'])
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @extend_schema(
#         summary="Получение комментария по id",
#         description="Получение комментария по id, доступен для всех",
#         request=CommentSerializer,
#         responses={
#             200: OpenApiResponse(response=CommentSerializer, description="Задачи успешно получены"),
#         }
#     )
# class CommentTaskProject(ListAPIView):
#     permission_classes = (AllowAny, )
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def get(self, request, *args, **kwargs):
#         comment = Comment.objects.get(task=kwargs.get('id_task'))
#         serializer = self.serializer_class(comment)
#         return Response(serializer.data, status=status.HTTP_200_OK)

















# class UserViewSet(viewsets.ModelViewSet):
#     queryset = DefaultUser.objects.all()

# class ProjectView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()
#
#     def get_object(self, id=None):
#         try:
#             return Project.objects.get(id=id)
#         except Project.DoesNotExist:
#             raise NotFound(detail="user не найдена")
#
#
#
#     def get(self, request, id=None):
#         """
#         Получить информацию о проектах или о проекте по ID если задан pk.
#         """
#
#         if id:
#             project = self.get_object(id)
#             if not project:
#                 return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
#             serializer = self.get_serializer(project)
#             return Response(serializer.data)
#         else:
#             projects = Project.objects.all()
#             serializer = self.get_serializer(projects, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Создать нового проекта.
#         """
#
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             #print(serializer.data)
#             # for idd in request.data.get('members'):
#             #     for user in DefaultUser.objects.all().filter(id=idd):
#             #         user.history_project += f'{request.data.get('title')} | '
#             #         user.save()
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, id=None):  # надо добавить сюда при добавлении нового пользоваателя что бы ему записывалось в history_proj
#         """
#         Обновить информацию о проекте.
#         """
#         user = self.get_object(id)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id=None):
#         """
#         Удалить проект по ID.
#         """
#         user = self.get_object(id)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class ProjectMembersView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()
#
#     def get_object(self, id=None):
#         try:
#             return Project.objects.get(id=id)
#         except Project.DoesNotExist:
#             raise NotFound(detail="project не найден")
#
#     def get(self, request, id=None):
#         """
#         Получить информацию о проектах или о проекте по ID если задан pk.
#         """
#         if id:
#             project = self.get_object(id)
#             if not project:
#                 return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
#             serializer = self.get_serializer(project)
#             return Response(serializer.data.get('members'))
#
#
#
#     def put(self, request, id=None):
#         """
#         Обновить информацию о проекте.
#         """
#         user = self.get_object(id)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id=None):
#         """
#         Удалить проект по ID.
#         """
#         user = self.get_object(id)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class RolesView(generics.RetrieveUpdateDestroyAPIView):  # надо дописать для правильного получения roles по конретному проекту (доп.)
#     serializer_class = RolesSerializer
#     queryset = Roles.objects.all()
#
#     def get_object(self, id=None):
#         try:
#             return Roles.objects.get(id=id)
#         except Roles.DoesNotExist:
#             raise NotFound(detail="user не найдена")
#
#
#
#     def get(self, request, id=None):
#         """
#         Получить информацию о проектах или о проекте по ID если задан id.
#         """
#
#         if id:
#             project = self.get_object(id)
#             if not project:
#                 return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
#             serializer = self.get_serializer(project)
#             return Response(serializer.data)
#         else:
#             projects = Roles.objects.all()
#             serializer = self.get_serializer(projects, many=True)
#             return Response(serializer.data)
#
#     def post(self, request,id=None):
#         """
#         Создать нового проекта.
#         """
#         serializer = RolesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, id=None):
#         """
#         Обновить информацию о проекте.
#         """
#         user = self.get_object(id)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id=None):
#         """
#         Удалить проект по ID.
#         """
#         user = self.get_object(id)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProjectMembersView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()
#
#     def get_object(self, pk=None):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise NotFound(detail="project не найден")
#
#     def get(self, request, pk=None):
#         """
#         Получить информацию о проектах или о проекте по ID если задан pk.
#         """
#         if pk:
#             project = self.get_object(pk)
#             if not project:
#                 return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
#             serializer = self.get_serializer(project)
#             return Response(serializer.data.get('members'))
#
#
#
#     def put(self, request, pk=None):
#         """
#         Обновить информацию о проекте.
#         """
#         user = self.get_object(pk)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk=None):
#         """
#         Удалить проект по ID.
#         """
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProjectListAPIView(ListAPIView):


