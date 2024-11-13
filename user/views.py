from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import DefaultUser
from .serializers import UserSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = DefaultUser.objects.all()
#     serializer_class = UserSerializer
#
#
#     @action(methods=['post'], detail=False) # эта хуета работает только через postman потму что не приниает get запросы
#     def registrate(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'post': 'Created user'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectAPIView(APIView):

    def get_object(self, UUID):
        print(UUID)
        try:
            return DefaultUser.objects.get(id=UUID)
        except DefaultUser.DoesNotExist:
            raise NotFound(detail="Книга не найдена")

    def get(self, request, UUID=None):
        """
        Получить информацию о проектах или о проекте по ID если задан pk.
        """
        if UUID:
            user = self.get_object(UUID)
            if not user:
                return Response({'error': 'Книгаeъуъъ не найдена'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            projects = DefaultUser.objects.all()
            serializer = UserSerializer(projects, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        Создать нового проекта.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Обновить информацию о проекте.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Удалить проект по ID.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
