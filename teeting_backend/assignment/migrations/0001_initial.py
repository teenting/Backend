
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, 'level1'), (2, 'level2'), (3, 'level3'), (4, 'level4'), (5, 'level5'), (6, 'level6'), (7, 'level7'), (8, 'level8'), (9, 'level9')])),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begDate', models.DateTimeField(default=datetime.datetime.now)),
                ('expDate', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.IntegerField(choices=[(0, 'fail'), (1, 'success'), (2, 'doing'), (3, 'finished')], default=2)),
                ('content', models.CharField(max_length=200)),
                ('reward', models.IntegerField()),
            ],
        ),
    ]
