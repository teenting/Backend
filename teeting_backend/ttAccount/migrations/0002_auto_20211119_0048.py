# Generated by Django 3.2.9 on 2021-11-18 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttAccount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='finCard',
        ),
        migrations.RemoveField(
            model_name='user',
            name='finCard',
        ),
        migrations.AddField(
            model_name='child',
            name='firstname',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='child',
            name='lastname',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
