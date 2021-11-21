from re import L

from django.db import models
from .models import User, Child
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
   class Meta:
    model = User
    fields = '__all__'
    

class ChildSerializer(serializers.ModelSerializer) :
   class Meta :
      model = Child
      fields = '__all__'

   
   