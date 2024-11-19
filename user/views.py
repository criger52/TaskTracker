from functools import partial

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import DefaultUser
from .serializers import UserSerializer



class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = DefaultUser.objects.all()

    def get_object(self, pk=None):
        try:
            return DefaultUser.objects.get(pk=pk)
        except DefaultUser.DoesNotExist:
            raise NotFound(detail="user не найдена")



    def get(self, request, pk=None):
        """
        Получить информацию о users или о user по ID если задан pk.
        """
        if pk:
            user = self.get_object(pk)

            if not user:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:

            users = DefaultUser.objects.all()
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)


    def post(self, request):
        """
        Создать нового user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Обновить информацию о user.
        """
        user = self.get_object(pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Удалить user по ID.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
