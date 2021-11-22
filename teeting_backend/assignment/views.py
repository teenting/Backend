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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    #해당 child에 대해서만 나오게 하려면
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method == "GET":
            if self.request.user.is_authenticated : # 로그인 유무
                childid = self.request.query_params.get("childId", None)
                # childid가 존재하고 현재 로그인 된 유저의 자식일때만 반영
                if childid is not None and Child.objects.filter(id=childid).first().parent == self.request.user:
                    qs = Mission.objects.filter(child_id=childid)
                else: 
                    qs = qs.none()
            else:
                qs = qs.none()
        return qs
 
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class AchievementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated : # 로그인 유무
            childid = self.request.query_params.get("childId", None)
            # childid가 존재하고 현재 로그인 된 유저의 자식일때만 반영
            if childid is not None and Child.objects.filter(id=childid).first().parent == self.request.user:
                qs = Achievement.objects.filter(child_id=childid)
            else: 
                qs = qs.none()
        else:
            qs = qs.none()
        return qs
