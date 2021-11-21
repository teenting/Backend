
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        ('ttAccount', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),


    operations = [
        migrations.AddField(
            model_name='mission',
            name='child',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mission', to='ttAccount.child'),
        ),
        migrations.AddField(
            model_name='mission',
            name='parent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievement',
            name='child',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='achievement_child', to='ttAccount.child'),
        ),
    ]
