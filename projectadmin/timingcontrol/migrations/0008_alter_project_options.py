# Generated by Django 3.2.9 on 2022-05-13 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timingcontrol', '0007_worker_usernameid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('can_mark_factured', 'can_mark_factured'),)},
        ),
    ]