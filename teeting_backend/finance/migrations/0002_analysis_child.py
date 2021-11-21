
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
