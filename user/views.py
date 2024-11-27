
from comment.models import Comment
from comment.seializers import CommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from project.serializers import *
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from task.models import Task
from task.serializers import TaskSerializer

from .models import DefaultUser
from .serializers import UserSerializer, RegistrationSerializer, UserProjectSerializer, UserProfileForAllSerializer


@extend_schema(
        summary="Регистрация нового пользователя",
        description="Регистрирует пользователя с заданными данными, доступен для всех",
        request=RegistrationSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно зарегистрирован"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        summary="Текущий аутентифицированный пользователь",
        description="Обращается к текущему аутентифицированному пользователю, доступен лишь для аутентифицированных пользователей",
        request=UserSerializer,
        responses={
            200: OpenApiResponse(response=UserProfileForAllSerializer, description="Пользователь успешно получен"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserProfileForAllSerializer

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@extend_schema(
        summary="Получает пользователя по id",
        description="Получает пользователя по id, доступен для всех",
        request=RegistrationSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно зарегистрирован"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class GetUserAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

@extend_schema(
        summary="Изменение/Удаление пользователя",
        description="Изменяет или удаляет текущего аутентифицированного, доступен для аутентифицированных",
        request=RegistrationSerializer,
        responses={
            200: OpenApiResponse(response=UserProfileForAllSerializer, description="Пользователь успешно изменен"),
            400: OpenApiResponse(description="Ошибки валидации"),
            204: OpenApiResponse(description="Пользователь успешно удален")
        }
    )
class DeleteUpdateUserAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserProfileForAllSerializer
    # lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True позволяет частично обновить данные
        if serializer.is_valid():
            serializer.save()  # Сохраняем изменения
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({'detail': 'user is deleted'}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(
        summary="Список ролей конкретного пользователя",
        description="Получает список ролей пользователя из url, доступен для всех",
        request=UserProjectSerializer,
    )
class ListProjectsUser(APIView):
    permission_classes = (AllowAny, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer


    def get(self, request, *args, **kwargs):
        user = DefaultUser.objects.all().get(id=kwargs.get('id_user'))
        serializer = UserSerializer(user)
        # print(serializer.data.get('role_in_proj'))
        projects = []
        for i in serializer.data.get('role_in_proj'):
            projects.append(i)
        return Response(projects)


@extend_schema(
        summary="Список ролей конкретного пользователя",
        description="Получает список ролей пользователя из url, доступен для всех",
        request=UserProjectSerializer,
    )
class ListProjectsCurrentUser(APIView):
    permission_classes = (AllowAny, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer


    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        # print(serializer.data.get('role_in_proj'))
        projects = []
        for i in serializer.data.get('role_in_proj'):
            projects.append(i)
        return Response(projects)

@extend_schema(
        summary="Получает проект по id",
        description="Получает проект по id, доступен для всех",
        request=UserProjectSerializer,
    )
class ProjectUserAPIView(APIView):
    permission_classes = (AllowAny, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id_project'))
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

@extend_schema(
        summary="Регистрация нового пользователя",
        description="Регистрирует пользователя с заданными данными, доступен для всех",
        request=RegistrationSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно зарегистрирован"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class TaskProjectUserAPIView(APIView):
    permission_classes = (AllowAny, )
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('id_task'))
        serializer = TaskSerializer(task)
        return Response(serializer.data)

@extend_schema(
        summary="Регистрация нового пользователя",
        description="Регистрирует пользователя с заданными данными, доступен для всех",
        request=RegistrationSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно зарегистрирован"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class CommentTaskProjectUserAPIView(APIView):
    permission_classes = (AllowAny, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs.get('id_comment'))
        serializer = CommentSerializer(comment)
        return Response(serializer.data)



