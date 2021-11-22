from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

# Create your models here.

# class User(AbstractUser):
#     birthday = models.CharField(max_length=8)
#     finAcno = models.CharField(max_length=200) #핀어카운트
#     acno = models.CharField(max_length=100) #계좌
#     iscd =models.CharField(max_length=20) #기관번호
#     accessToken = models.CharField(max_length=200) #토큰


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username :
            raise ValueError('Username must be set')
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin) :

    username = models.CharField(max_length=30, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    birthday = models.CharField(max_length=8)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    finAcno = models.CharField(max_length=200, null=True, blank=True) #핀어카운트
    acno = models.CharField(max_length=100, null=True, blank=True) #계좌
    iscd =models.CharField(max_length=20, null=True, blank=True) #기관번호
    accessToken = models.CharField(max_length=200, null=True, blank=True) #토큰

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'



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