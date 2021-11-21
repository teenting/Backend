from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Mission, Achievement

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'
class AchievementSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Achievement
        fields = '__all__'