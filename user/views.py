from functools import partial
from symtable import Class

from PIL.ImageOps import posterize
from django.contrib.auth import authenticate
from django.contrib.staticfiles.views import serve
from django.core.serializers import get_serializer
from django.shortcuts import render
# from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from comment.models import Comment
from comment.seializers import CommentSerializer
from project.models import Project
from task.models import Task
from project.serializers import ProjectSerializer, ProjectTitleIDSerializers
from task.serializers import TaskSerializer
from .models import DefaultUser
from .serializers import UserSerializer, RegistrationSerializer, UserProfileForAllSerializer, UserProjectSerializer


#
# class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserSerializer
#     queryset = DefaultUser.objects.all()
#
#     def get_object(self, pk=None):
#         try:
#             return DefaultUser.objects.get(pk=pk)
#         except DefaultUser.DoesNotExist:
#             raise NotFound(detail="user не найдена")
#
#
#
#     def get(self, request, pk=None):
#         """
#         Получить информацию о users или о user по ID если задан pk.
#         """
#
#         if pk:
#             user = self.get_object(pk)
#
#             if not user:
#                 return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
#
#             serializer = self.get_serializer(user)
#             return Response(serializer.data)
#         else:
#
#             users = DefaultUser.objects.all()
#             serializer = self.get_serializer(users, many=True)
#             return Response(serializer.data)
#
#
#     def post(self, request):
#         """
#         Создать нового user.
#         """
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk=None):
#         """
#         Обновить информацию о user.
#         """
#         user = self.get_object(pk)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Удалить user по ID.
#         """
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
#


# classlass APIView(CreateAPIView):
#     permission_classes = []
#
#     def get(self, request):
#         pass


# class UserAPIView(APIView):
#     serializer_class = UserSerializer
#
#     def get(self, request):
#         users = DefaultUser.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

# @extend_schema(
#         summary="Регистрация нового пользователя",
#         description="Регистрирует пользователя с заданными данными",
#         request=RegistrationSerializer,
#         responses={
#             201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно зарегистрирован"),
#             400: OpenApiResponse(description="Ошибки валидации")
#         }
#     )
class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'registration has been completed'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @extend_schema(
#         summary="Текущий аутентифицированный пользователь",
#         description="Обращается к текущему аутентифицированному пользователю",
#         request=UserSerializer,
#         responses={
#             200: OpenApiResponse(response=UserSerializer, description="Пользователь успешно получен"),
#             400: OpenApiResponse(description="Ошибки валидации")
#         }
#     )
class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "user is updated"}, status=status.HTTP_200_OK)
        return Response({"detail": "not valid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'detail': 'user is deleted'}, status=status.HTTP_204_NO_CONTENT)



class GetUserAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = DefaultUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

class DeleteUpdateUserAPIView(APIView):
    permission_classes = [AllowAny]  # нужно что бы текущий аутентифицированный пользователь совпадал по айди с изменяемым lj,fdm fynetnbabwbhjdyyjcnm
    queryset = DefaultUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        user = DefaultUser.objects.all().filter(id=request.id_user).first()  # Получаем пользователя по id

        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True позволяет частично обновить данные

        if serializer.is_valid():
            serializer.save()  # Сохраняем изменения
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass


class ListUserAPIView(ListAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    queryset = DefaultUser.objects.all()
    serializer_class = UserSerializer

class ListProjectsUser(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer


    def get(self, request, *args, **kwargs):
        return Response(ProjectTitleIDSerializers(UserSerializer(DefaultUser.objects.all().filter(username=request.user).first()).data.get('projects'), many=True).data)


class ProjectUserAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer

    def get(self, request, id_project=None, *args, **kwargs):
        project = Project.objects.all().filter(id=id_project).first()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class TaskProjectUserAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = DefaultUser.objects.all()
    serializer_class = UserProjectSerializer

    def get(self, request, id_task=None, *args, **kwargs):
        task = Task.objects.all().filter(id=id_task).first()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

class CommentTaskProjectUserAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, id_comment=None, *args, **kwargs):
        comment = Comment.objects.all().filter(id=id_comment).first()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


