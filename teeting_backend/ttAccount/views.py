from rest_framework import generics, viewsets
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *

class UserInfoViewSet(viewsets.ModelViewSet) :
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(username = self.request.user)
        else :
            qs = qs.none()
        return qs

class ChildInfoViewSet(viewsets.ModelViewSet) :
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(parent = self.request.user)
        else :
            qs = qs.none()
        return qs
