# Generated by Django 2.2.4 on 2019-08-07 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_auto_20190805_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='home_phone',
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, help_text='Enter your first and last name', max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, help_text='Enter your main phone number', max_length=10),
        ),
        migrations.CreateModel(
            name='UserContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(blank=True, max_length=200)),
                ('contact_phone', models.CharField(blank=True, max_length=10)),
                ('contact_email', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
