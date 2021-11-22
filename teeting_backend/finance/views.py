from django.utils import datastructures
from rest_framework import serializers, viewsets, authentication, status
from rest_framework.exceptions import bad_request
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

# Create your views here.


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
            return HttpResponse("No User", res.status_code)

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
                return HttpResponse("No child", res.status_code)
        return HttpResponse(json.dumps(data), content_type="text/json-comment-filtered", status = status.HTTP_200_OK)


# 거래내역 조회 -> params가 있다면 자녀거래내역 조회 / 없다면 유저(부모)의 거래내역 조회
class TransactionView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        url = 'https://developers.nonghyup.com/InquireTransactionHistory.nh' # 거래내역 조회 url
        user = User.objects.filter(username = self.request.user).first()
        childId = self.request.query_params.get('childId')
        
        # params로 받은 childId값이 없다면 유저거래내역 조회
        if not childId :
            apiNm = url[url.find(".com/")+5:url.find(".nh")]
            tsymd = datetime.today().strftime("%Y%m%d")
            trtm = "112428"
            iscd = user.iscd
            fintechApsno = "001"
            apiSvcCd = "ReceivedTransferA"
            # isTuno =  임의번호로 채번
            accessToken = user.accessToken
            bncd = "011" # 농협은행코드 고정값
            acno = user.acno
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
            
        # params로 받은 childId값이 있다면 유저거래내역 조회
        else :
            child = Child.objects.filter(parent = user).filter(pk = childId).first()

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
            return HttpResponse("No User or No Child", res.status_code)


# 자녀 분석결과 조회
class ChildAnalysisView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def get(self, request):

        # 프론트에 response로 줄 json data
        data = {}
        childId = self.request.query_params.get('childId')
        child = Child.objects.filter(pk = childId).first()
        period = self.request.query_params.get('period')

        if not child :
            return HttpResponse("You don't have such child", status=status.HTTP_400_BAD_REQUEST)

        # 필터링할 날짜 범위 지정
        if period == "week" :
            start_date = datetime.now().date() + relativedelta(days=-7)
        elif period == "month" :
            start_date = datetime.now().date() + relativedelta(months=-1)
        elif period == "semiannual" :
            start_date = datetime.now().date() + relativedelta(months=-6)
        elif period == "annual" :
            start_date = datetime.now().date() + relativedelta(years=-1)
        else : 
            return HttpResponse("Period is uncorrect", status=status.HTTP_400_BAD_REQUEST)

        spending = Analysis.objects.filter(child = child).filter(date__range = [start_date, datetime.now().date()])


        # initializing
        food = 0 # 0번 카테고리
        transportation = 0 # 1번 카테고리
        hobby = 0 # 2번 카테고리
        etc = 0 # 3번 카테고리

        for i in range(len(spending)) :
            if spending[i].category == 0 :
                food += spending[i].tram

            elif spending[i].category ==  1 :
                transportation += spending[i].tram

            elif spending[i].category ==  2 :
                hobby += spending[i].tram

            elif spending[i].category ==  3 :
                etc += spending[i].tram
            
        data["food"] = food
        data["transportation"] = transportation
        data["hobby"] = hobby
        data["etc"] = etc
        data["total"] = food + transportation + hobby + etc

        if self.request.user.is_authenticated :
            return HttpResponse(json.dumps(data), content_type="text/json-comment-filtered", status=status.HTTP_200_OK)
        else :
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)



class RemittanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        user = User.objects.filter(username = self.request.user).first()
        childid = self.request.query_params.get("childId", None)
        if childid is not None:
            child = Child.objects.filter(id=childid).first()
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        url_drawing = "https://developers.nonghyup.com/DrawingTransfer.nh" # 출금 이체 url

        apiNm = url_drawing[url_drawing.find(".com/")+5 : url_drawing.find(".nh")]
        tsymd = datetime.today().strftime("%Y%m%d")
        trtm = "112428"
        iscd = user.iscd
        fintechApsno = "001"
        apiSvcCd = "ReceivedTransferA"
        # isTuno =  임의번호로 채번
        accessToken = user.accessToken
        finAcno = user.finAcno
        tram = self.request.POST['tram']
        dractOtlt = child.lastname + child.firstname #출금인자내용

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
            "FinAcno": finAcno,
            "Tram" : tram,
            "DractOtlt" : dractOtlt
        }
        res = requests.post(url_drawing, data=json.dumps(body), headers=headers)
        if res.status_code == 200 :
            #출금성공, 입금
            url_receive = "https://developers.nonghyup.com/ReceivedTransferAccountNumber.nh" # 출금 이체 url

            apiNm = url_receive[url_receive.find(".com/")+5 : url_receive.find(".nh")]
            tsymd = datetime.today().strftime("%Y%m%d")
            trtm = "112428"
            iscd = child.iscd
            fintechApsno = "001"
            apiSvcCd = "ReceivedTransferA"
            # isTuno =  임의번호로 채번
            accessToken = child.accessToken
            bncd = "011"
            acno = child.acno
            tram = self.request.POST['tram']
            dractOtlt = child.lastname + child.firstname #출금인자내용
            mractOtlt = user.username

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
                "Bncd" : bncd,
                "Acno" : acno,
                "Tram" : tram,
                "DractOtlt" : dractOtlt,
                "MractOtlt" : mractOtlt
            }
            res = requests.post(url_receive, data=json.dumps(body), headers=headers)
            if res.status_code == 200 :
                return HttpResponse("remittance successed", status = status.HTTP_200_OK)
            else:
                return HttpResponse("drawed but not transferred error", res.status_code) #출금은 되었는데 입금이 안됨.... 나중에 핸들링 필요
        else :
            #출금실패
            return HttpResponse("not drawed",res.status_code)
