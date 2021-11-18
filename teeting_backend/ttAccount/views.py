from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    qureyset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset()

class UserChildView(APIView):

    def get(self, request):
        user = User.objects.filter(user=self.request.user)
        serializers = UserSerializer
