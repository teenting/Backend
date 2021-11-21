from django.http import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets

from ttAccount.models import Child
from .models import Mission, Achievement
from .serializers import MissionSerializer, AchievementSerializer
# Create your views here.

class MissionViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    #해당 child에 대해서만 나오게 하려면

    def get_queryset(self):
        qs = super().get_queryset()
        childid = self.request.query_params.get("childId", None)
        if childid is not None:
            qs = Mission.objects.filter(child_id=childid)
        return qs

class AchievementViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        childid = self.request.query_params.get("childId", None)
        if childid is not None:    
            qs = Achievement.objects.filter(child_id=childid)
        return qs