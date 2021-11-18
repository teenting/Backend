from django.db.models import fields
from rest_framework import serializers
from .models import *

class AnalysisSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Analysis
        fields = '__all__'