# Generated by Django 3.2.9 on 2022-05-25 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timingcontrol', '0013_auto_20220522_2233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useres',
            options={'ordering': ['last_name']},
        ),
        migrations.CreateModel(
            name='Times',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('timeEntry', models.TimeField(blank=True, null=True)),
                ('timeExit', models.TimeField(blank=True, null=True)),
                ('worked_hours', models.FloatField(blank=True, default=0, null=True)),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='timingcontrol.project')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='timingcontrol.useres')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
