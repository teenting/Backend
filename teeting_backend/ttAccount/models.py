from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    birthday = models.CharField(max_length=8)
    isParent = models.BooleanField(default=False)
    finAcno = models.CharField(max_length=200)
    finCard = models.CharField(max_length=200)
    acno = models.CharField(max_length=100)
    iscd =models.CharField(max_length=20)
    accessToken = models.CharField(max_length=200)


class Family(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_parent')
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_child')