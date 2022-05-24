# Generated by Django 3.2.9 on 2022-05-10 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timingcontrol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='latitude_max',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='Set here latitude max', max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='latitude_min',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='Set here latitude min', max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='longitude_max',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='Set here longitude max', max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='longitude_min',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='Set here longitude min', max_digits=20, null=True),
        ),
    ]
