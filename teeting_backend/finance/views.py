from django.utils import datastructures
from rest_framework import serializers, viewsets, authentication, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import *
from .serializers import *
from ttAccount.models import User, Child

import requests
import json

from datetime import datetime
from dateutil.relativedelta import relativedelta

import random
from django.http import HttpResponse
from django.core import serializers

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


# 잔액조회 (부모)
class ParentBalanceView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
                "IsTuno": "0007773" + str(random.randint(0,10000)), # isTuno
                "AccessToken": accessToken
            },
            "FinAcno": finAcno
        }

        res = requests.post(url, data=json.dumps(body), headers=headers)
        data = {}
        if res.status_code == 200 :
            data["id"] = self.request.user.id
            data["username"] = self.request.user.username
            data["acno"] = self.request.user.acno
            data["balance"] = int(res.json()["Ldbl"])
            return HttpResponse(json.dumps(data), content_type="text/json-comment-filtered", status = status.HTTP_200_OK)
        else :
            return HttpResponse(res.status_code)

# 잔액조회 (자녀)
class ChildBalanceView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        currentUser = User.objects.filter(username = self.request.user).first()
        children = Child.objects.filter(parent = currentUser)

        # 프론트에 response로 줄 json data
        data = []

        # 자녀 수만큼 api 반복 호출
        for i in range(len(children)) :
            url = "https://developers.nonghyup.com/InquireBalance.nh" # 잔액 조회 url

            apiNm = url[url.find(".com/")+5 : url.find(".nh")]
            tsymd = datetime.today().strftime("%Y%m%d")
            trtm = "112428"
            iscd = children[i].iscd
            fintechApsno = "001"
            apiSvcCd = "ReceivedTransferA"
            # isTuno =  임의번호로 채번
            accessToken = children[i].accessToken
            finAcno = children[i].finAcno
            
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
                    "IsTuno": "0007773" + str(random.randint(0,10000)), # isTuno
                    "AccessToken": accessToken
                },
                "FinAcno": finAcno
            }

            res = requests.post(url, data=json.dumps(body), headers=headers)
            children_data = {}
            if res.status_code == 200 :
                children_data["id"] = children[i].id
                children_data["firstname"] = children[i].firstname
                children_data["parent"] = children[i].parent.username
                children_data["balance"] = int(res.json()["Ldbl"])
                data.append(children_data)
            else :
                return HttpResponse(res.status_code)
        return HttpResponse(json.dumps(data), content_type="text/json-comment-filtered", status = status.HTTP_200_OK)



# 자녀 거래내역 조회
class ChildTransactionView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        childId = self.request.query_params.get('childId')
        currentUser = User.objects.filter(username = self.request.user).first()
        child = Child.objects.filter(parent = currentUser).filter(pk = childId).first()

        url = 'https://developers.nonghyup.com/InquireTransactionHistory.nh' # 거래내역 조회 url

        apiNm = url[url.find(".com/")+5:url.find(".nh")]
        tsymd = datetime.today().strftime("%Y%m%d")
        trtm = "112428"
        iscd = child.iscd
        fintechApsno = "001"
        apiSvcCd = "ReceivedTransferA"
        # isTuno =  임의번호로 채번
        accessToken = child.accessToken
        bncd = "011" # 농협은행코드 고정값
        acno = child.acno
        insymd = (datetime.today() + relativedelta(days=-90)).strftime("%Y%m%d")
        ineymd = datetime.today().strftime("%Y%m%d")
        trnsDsnc = "A"
        lnsq = "DESC"
        pageNo = "1"
        dmcnt = "100"
        
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
                "IsTuno": "0007773" + str(random.randint(0,10000)), # isTuno
                "AccessToken": accessToken
            },
            "Bncd": bncd,
            "Acno": acno,
            "Insymd": insymd,
            "Ineymd": ineymd,
            "TrnsDsnc": trnsDsnc,
            "Lnsq": lnsq,
            "PageNo": pageNo,
            "Dmcnt": dmcnt
        }

        # 프론트에 response로 줄 json data
        data = []

        res = requests.post(url, data=json.dumps(body), headers=headers)
        if res.status_code == 200 :
            rec = res.json()["REC"]

            for i in range(len(rec)) :
                transactions = {}
                transactions["trdd"] = rec[i]["Trdd"]
                transactions["txtm"] = rec[i]["Txtm"]
                transactions["mnrcDrotDsnc"] = int(rec[i]["MnrcDrotDsnc"])
                transactions["tram"] = int(rec[i]["Tram"])
                transactions["aftrBlnc"] = int(rec[i]["AftrBlnc"])
                transactions["bnprCntn"] = rec[i]["BnprCntn"]
                transactions["tuno"] = int(rec[i]["Tuno"])
                data.append(transactions)
            return HttpResponse(json.dumps(data), content_type="text/json-comment-filtered", status = status.HTTP_200_OK)

        else :
            return HttpResponse(res.status_code)