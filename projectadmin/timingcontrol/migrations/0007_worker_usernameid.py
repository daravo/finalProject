# Generated by Django 3.2.9 on 2022-05-13 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timingcontrol', '0006_alter_worker_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='usernameid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
