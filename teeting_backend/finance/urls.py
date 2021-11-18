from django.urls import path
from .views import *


analysis_list = AnalysisViewSet.as_view({
    'get' : 'list',
    'post' : 'create'
})

analysis_detail = AnalysisViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy',
})

urlpatterns = [

    path('analysis/', analysis_list),
    path('analysis/<int:pk>', analysis_detail),
    path('balance', InquireBalanceView.as_view()), # 잔액조회
]