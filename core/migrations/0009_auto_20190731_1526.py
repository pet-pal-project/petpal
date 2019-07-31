# Generated by Django 2.2.3 on 2019-07-31 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190730_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('checklist_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Checklist')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitter_id', models.CharField(max_length=50)),
                ('due_date_on', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='routine',
            name='assigned_pet',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='assigned_sitter',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='sitter',
        ),
        migrations.AddField(
            model_name='pet',
            name='age',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.DeleteModel(
            name='Critical',
        ),
        migrations.DeleteModel(
            name='Routine',
        ),
        migrations.AddField(
            model_name='checklist',
            name='pet_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pet'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='visits',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Visit'),
        ),
    ]