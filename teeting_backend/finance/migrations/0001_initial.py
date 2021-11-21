
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('tram', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('bnprCntn', models.TextField()),
                ('tuno', models.IntegerField()),
                ('category', models.IntegerField(choices=[(0, '식비'), (1, '교통비'), (2, '문화생활비'), (3, '기타')], default=0)),
            ],
        ),
    ]
