# Generated by Django 2.2.3 on 2019-07-29 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_routine_assigned_sitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='home_phone',
            field=models.CharField(blank=True, max_length=9),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=9),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_phone',
            field=models.CharField(blank=True, max_length=9),
        ),
    ]
