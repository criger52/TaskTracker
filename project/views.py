from functools import partial

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = DefaultUser.objects.all()

class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_object(self, pk=None):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(detail="user не найдена")



    def get(self, request, pk=None):
        """
        Получить информацию о проектах или о проекте по ID если задан pk.
        """
        if pk:
            project = self.get_object(pk)
            if not project:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        else:
            projects = Project.objects.all()
            serializer = self.get_serializer(projects, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        Создать нового проекта.
        """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Обновить информацию о проекте.
        """
        user = self.get_object(pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Удалить проект по ID.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
