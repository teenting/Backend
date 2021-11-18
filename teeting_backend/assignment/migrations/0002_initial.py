# Generated by Django 3.2.9 on 2021-11-18 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mission', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievement',
            name='child',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='achievement_child', to=settings.AUTH_USER_MODEL),
        ),
    ]
