# Generated by Django 3.2.9 on 2021-11-18 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
        ('ttAccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='child',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ttAccount.child'),
        ),
    ]
