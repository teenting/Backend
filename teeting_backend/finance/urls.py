from django.urls import path
from .views import *


# analysis_list = AnalysisViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create'
# })

# analysis_detail = AnalysisViewSet.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy',
# })

urlpatterns = [

    # path('analysis/', analysis_list),
    # path('analysis/<int:pk>', analysis_detail),


    path('analysis/', ChildAnalysisView.as_view()), # 자녀분석 조회 ?childId=<int>
    path('balance/', ParentBalanceView.as_view()), # 잔액조회 부모
    path('balance/child', ChildBalanceView.as_view()), # 잔액조회 자녀
    path('transaction/', ChildTransactionView.as_view()), # 거래내역조회 자녀 ?childId=<int>&period=<string>
]