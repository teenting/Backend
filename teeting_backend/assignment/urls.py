from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from assignment import views

router = DefaultRouter()
router.register(r'mission', views.MissionViewSet, basename='mission')
router.register(r'achievement', views.AchievementViewSet, basename='achievement')

urlpatterns = [
    path('', include(router.urls))
]