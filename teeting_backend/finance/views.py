from rest_framework import serializers, viewsets, authentication, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import *
from .serializers import *
from ttAccount.models import User

import requests
import json

from datetime import datetime
import random
from django.http import HttpResponse

# Create your views here.


# 분석작업 기본적인 CRUD 구현 변경 많이많이 필요함
class AnalysisViewSet(viewsets.ModelViewSet) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def perform_create(self, serializer):
        serializer.save(child = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(child = self.request.user)
        else :
            qs = qs.none()
        return qs


# 잔액 조회 GET 버전   
class InquireBalanceView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # 부모는 get으로 조회
    def get(self, request):
        user = User.objects.filter(username = self.request.user).first()
        
        url = "https://developers.nonghyup.com/InquireBalance.nh" # 잔액 조회 url

        apiNm = url[url.find(".com/")+5 : url.find(".nh")]
        tsymd = datetime.today().strftime("%Y%m%d")
        trtm = "112428"
        iscd = user.iscd
        fintechApsno = "001"
        apiSvcCd = "ReceivedTransferA"
        # isTuno =  임의번호로 채번
        accessToken = user.accessToken
        finAcno = user.finAcno
        
        headers = {
            "Content-Type": "application/json; chearset=utf-8",
        }

        body = {
            "Header": {
                "ApiNm": apiNm,
                "Tsymd": tsymd,
                "Trtm": trtm,
                "Iscd": iscd,
                "FintechApsno": fintechApsno,
                "ApiSvcCd": apiSvcCd,
                "IsTuno": "0007770", # isTuno
                "AccessToken": accessToken
            },
            "FinAcno": finAcno
        }

        res = requests.post(url, data=json.dumps(body), headers=headers)
        if res.status_code == 200 :
            print(res.json()["Ldbl"])
            return HttpResponse(res.json()["Ldbl"], status = status.HTTP_200_OK)
        else :
            return HttpResponse(res.status_code)





