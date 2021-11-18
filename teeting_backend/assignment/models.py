from django.db import models
from django.db.models.deletion import CASCADE
from django.urls.resolvers import _PATH_PARAMETER_COMPONENT_RE
from ttAccount.models import User, Family
from datetime import datetime
# Create your models here.

class Mission(models.Model):
    family = models.ForeignKey(Family, on_delete=CASCADE, related_name='mission_family')
    begDate = models.DateTimeField(default=datetime.now)
    expDate = models.DateTimeField(default=datetime.now)
    isFinished = models.BooleanField(default=False)
    content = models.CharField(max_length=200)
    reward = models.IntegerField()
    isTransferred = models.BooleanField(default=False)

    def __str__(self):
        return self.content
        
class Achievement(models.Model):
    LEVEL_CHOICES = (
        (1, 'level1'),
        (2, 'level2'),
        (3, 'level3'),
        (4, 'level4'),
        (5, 'level5'),
        (6, 'level6'),
        (7, 'level7'),
        (8, 'level8'),
        (9, 'level9')
    )
    child = models.OneToOneField(User, on_delete=CASCADE, related_name='achievement_child')
    level = models.IntegerField(choices=LEVEL_CHOICES)
    score = models.IntegerField()
