# Generated by Django 5.0.4 on 2024-04-25 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drivers',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='feldshers',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='meds',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='drivers',
            name='second_name',
        ),
        migrations.RemoveField(
            model_name='drivers',
            name='third_name',
        ),
        migrations.RemoveField(
            model_name='feldshers',
            name='second_name',
        ),
        migrations.RemoveField(
            model_name='feldshers',
            name='third_name',
        ),
        migrations.RemoveField(
            model_name='meds',
            name='second_name',
        ),
        migrations.RemoveField(
            model_name='meds',
            name='third_name',
        ),
        migrations.AddField(
            model_name='cars',
            name='mark',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cars',
            name='number',
            field=models.CharField(max_length=255, null=True),
        ),
    ]