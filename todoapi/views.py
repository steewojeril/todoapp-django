from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from todoapi.serializers import TodoSerializer
from todoapplication.models import Todo
from rest_framework import authentication,permissions

class TodosView(ModelViewSet):
    queryset=Todo.objects.all()
    serializer_class=TodoSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)