
from comment.models import Comment
from comment.seializers import CommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .permissions import IsUserInProjectOrCreator
from .serializers import TaskCreate, TaskInProjectSerializer


@extend_schema(
        summary="Создает новый задачу",
        description="Создает новую задачу, доступен для аутентифицированных",
        request=TaskCreate,
    )
class TaskCreate(CreateAPIView):
    permission_classes = (IsUserInProjectOrCreator, )
    queryset = Task.objects.all()
    serializer_class = TaskCreate

class TaskAllList(ListAPIView):
    # permission_classes = (, )
    permission_classes = (IsAdminUser,)
    queryset = Task.objects.all()
    serializer_class = TaskInProjectSerializer
@extend_schema(
        summary="Получает задачу по id",
        description="Получает задачу по id, доступен для всех",
        request=TaskInProjectSerializer,
    )
class TaskByID(APIView):
    permission_classes = (AllowAny,)
    queryset = Task.objects.all()
    serializer_class = TaskInProjectSerializer

    def get(self, request, *args, **kwargs):
        print(kwargs.get('id'))
        task = Task.objects.get(id=kwargs.get('id'))
        serializer = TaskInProjectSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
        summary="Изменяет/удаляет задачу по id",
        description="Изменяет/удаляет задачу по id, доступен для создателя",
        request=TaskInProjectSerializer,
        responses={
            200: OpenApiResponse(response=TaskInProjectSerializer, description="Задача успешно изменена"),
            201: OpenApiResponse(description='Пользователь успешно удален'),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class TaskByIDEdit(APIView):
    permission_classes = (IsUserInProjectOrCreator,)
    queryset = Task.objects.all()
    serializer_class = TaskInProjectSerializer

    def patch(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('id'))
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('id'))
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@extend_schema(
        summary="Получает все комментарии конкретной задачи",
        description="Изменяет/удаляет задачу по id, доступен для создателя",
        request=CommentSerializer,
    )
class CommentTask(APIView):
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(task=kwargs.get('id'))
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



