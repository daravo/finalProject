# Generated by Django 3.2.9 on 2022-06-12 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timingcontrol', '0014_auto_20220525_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='times',
            name='timeExit',
            field=models.TimeField(blank=True, default='00:00', null=True),
        ),
        migrations.AlterField(
            model_name='times',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='times',
            name='worked_hours',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
