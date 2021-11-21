from django.urls import path
from .views import *
from rest_auth.views import (LoginView, LogoutView)
from rest_auth.registration.views import RegisterView

user_info = UserInfoViewSet.as_view({
    'get' : 'list',
})

child_list = ChildInfoViewSet.as_view({
    'get': 'list',
})

child_detail = ChildInfoViewSet.as_view({
    'get': 'retrieve', 
    'put': 'update', 
    'patch': 'partial_update', 
    'delete': 'destroy', 
})

urlpatterns = [
    
    path('user/', user_info),
    path('child/', child_list),
    path('child/<int:pk>', child_detail),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('register', RegisterView.as_view()),
]