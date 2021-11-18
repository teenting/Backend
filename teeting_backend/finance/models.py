from django.core import validators
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import translation
from ttAccount.models import *
from django.core import validators

# Create your models here.

# 분석 모델
class Analysis(models.Model) :
    child = models.ForeignKey(Child, on_delete=CASCADE, default=1)
    trdd = models.CharField(max_length=8) # 거래날짜
    txtm = models.CharField(max_length=6) # 거래시간
    mnrcDrotDsnc = models.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(4)]) # 1,2는 입금 / 3,4는 출금
    tram = models.IntegerField(validators = [validators.MinValueValidator(0)]) # 거래금액
    aftrBlnc = models.IntegerField() # 거래후잔액
    bnprCntn = models.TextField() # 통장인자내용
    tuno = models.IntegerField() # 거래고유번호
    CATEGORIIES = (
        (0, "식비"),
        (1, "교통비"),
        (2, "문화생활비"),
        (3, "기타")
    )
    category = models.IntegerField(default=0, choices=CATEGORIIES)

    def __str__(self):
        return self.tuno