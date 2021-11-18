from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
# Create your models here.

class User(AbstractUser):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='user_child')
    birthday = models.CharField(max_length=8)
    finAcno = models.CharField(max_length=200)
    finCard = models.CharField(max_length=200)
    acno = models.CharField(max_length=100)
    iscd =models.CharField(max_length=20)
    accessToken = models.CharField(max_length=200)
