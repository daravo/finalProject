# Generated by Django 3.2.9 on 2022-05-10 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timingcontrol', '0004_project_lat_long'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='city',
            field=models.CharField(blank=True, help_text='Set here the name of the project', max_length=200, null=True),
        ),
    ]
