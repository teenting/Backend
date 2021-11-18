from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
# Create your models here.

class User(AbstractUser):
    birthday = models.CharField(max_length=8)
    finAcno = models.CharField(max_length=200) #핀어카운트
    acno = models.CharField(max_length=100) #계좌
    iscd =models.CharField(max_length=20) #기관번호
    accessToken = models.CharField(max_length=200) #토큰


class Child(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    parent = models.ForeignKey(User, on_delete=CASCADE)
    birthday = models.CharField(max_length=8)
    finAcno = models.CharField(max_length=200)
    acno = models.CharField(max_length=100)
    iscd =models.CharField(max_length=20)
    accessToken = models.CharField(max_length=200)

    def __str__(self):
        return self.firstname