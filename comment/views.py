
from comment.models import Comment
from comment.permissions import IsCreatorTask, IsCreatorComment
from comment.seializers import CommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
        summary="Создание комментария",
        description="Создает комментарий, доступен для создателя задачи",
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(response=CommentSerializer, description="Комментарий успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class CreateComment(CreateAPIView):
    permission_classes = (IsCreatorTask ,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
@extend_schema(
        summary="Получение комментария по id",
        description="Получает комментария по id, доступен для всех",
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(response=CommentSerializer, description="Комментарий успешно получен"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
class CommentByID(RetrieveAPIView):
    permission_classes = (AllowAny, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'


@extend_schema(
        summary="Изменение/удаление комментария по id",
        description="Изменение/удаление комментария по id, доступен для создателей комментария",
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(response=CommentSerializer, description="Комментарий успешно изменен"),
            400: OpenApiResponse(description="Ошибки валидации"),
            204: OpenApiResponse(description="Комментарий успешно удален")
        }
    )
class CommentByIDEdit(APIView):
    permission_classes = (IsCreatorComment,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs.get('id'))
        serializer = self.serializer_class(comment, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs.get('id'))
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





