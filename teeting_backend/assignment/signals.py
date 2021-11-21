from django.db.models.signals import post_save
from django.core.signals import request_started
from django.db.models import F
from django.dispatch import receiver
from .models import Mission, Achievement
from datetime import datetime
# mission이 finished (& transferred..?) 되면 achievement의 score가 update
# achievement의 score가 update되면 achievement의 level이 update
@receiver(post_save, sender=Mission)
def update_achievement_score(sender, **kwargs):
    childid = kwargs['instance'].child_id
    status = kwargs['instance'].status
    reward = kwargs['instance'].reward
    try:
        if status == 3:
            Achievement.objects.filter(child_id=childid).update(score=F('score') + (reward * 0.1))
    except:
        pass
@receiver(post_save, sender=Achievement)
def update_achievement_level(sender, **kwargs):
    childid = kwargs['instance'].child_id
    score = kwargs['instance'].score
    try:
        if score < 500:
            Achievement.objects.filter(child_id=childid).update(level=1)
        elif score < 1000:
            Achievement.objects.filter(child_id=childid).update(level=2)
        elif score < 1500:
            Achievement.objects.filter(child_id=childid).update(level=3)
        elif score < 2000:
            Achievement.objects.filter(child_id=childid).update(level=4)
        elif score < 2500:
            Achievement.objects.filter(child_id=childid).update(level=5)
        elif score < 3000:
            Achievement.objects.filter(child_id=childid).update(level=6)
        elif score < 3500:
            Achievement.objects.filter(child_id=childid).update(level=7)
        elif score < 4000:
            Achievement.objects.filter(child_id=childid).update(level=8)
        else:
            Achievement.objects.filter(child_id=childid).update(level=9)
    except:
        pass

# 현재 접근 시간보다 mission의 expDate가 이전이면 status를 fail로 
@receiver(request_started)
def date_expire(sender, **kwargs):
    current = datetime.now().date()
    try:
        for mission in list(Mission.objects.all()):
            if mission.status == 2 and mission.expDate.date() < current:
                mission.status = 0 #fail
                mission.save()
    except:
        print('error')