# Generated by Django 5.0.4 on 2024-04-25 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_typecars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='mark',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cars',
            name='number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cars',
            name='type',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='typecars',
            name='type',
            field=models.CharField(max_length=255),
        ),
    ]
