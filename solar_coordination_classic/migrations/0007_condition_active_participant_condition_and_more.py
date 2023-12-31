# Generated by Django 4.1.5 on 2023-11-20 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solar_coordination_classic', '0006_auto_20231116_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='condition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solar_coordination_classic.condition'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='participant',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='condition',
            unique_together={('ui_type', 'group_size')},
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='name',
        ),
    ]
