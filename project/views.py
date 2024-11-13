from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import Project
from .serializers import ProjectSerializer


class ProjectAPIView(APIView):
    def get(self, request, pk):
        """
        Получить информацию о проектах или о проекте по ID если задан pk.
        """
        if pk:
            project = Project.objects.filter(pk=pk).first()
            if not project:
                return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
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

    def put(self, request, pk):
        """
        Обновить информацию о проекте.
        """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Удалить проект по ID.
        """
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



