# Generated by Django 2.2.3 on 2019-07-31 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190731_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checklist',
            old_name='visits',
            new_name='visit',
        ),
    ]