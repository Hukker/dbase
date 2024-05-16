# Generated by Django 4.2.13 on 2024-05-16 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brigade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worktimestart', models.TimeField(max_length=255)),
                ('worktimeend', models.TimeField(max_length=255)),
                ('number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('реанимация', 'реанимация'), ('обычная', 'обычная')], max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('mark', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WorkersInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startwork', models.DateField(max_length=255)),
                ('startsickness', models.DateField(max_length=255, null=True)),
                ('startvacition', models.DateField(max_length=255, null=True)),
                ('endvacition', models.DateField(max_length=255, null=True)),
                ('endsickness', models.DateField(max_length=255, null=True)),
                ('endwork', models.DateField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('фельдшер', 'фельдшер'), ('медсестра', 'медсестра'), ('водитель', 'водитель')], max_length=255)),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.workersinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('adress', models.CharField(max_length=255)),
                ('result', models.CharField(choices=[('умер', 'умер'), ('везем в больницу', 'везем в больницу'), ('оказано лечение', 'оказано лечение')], max_length=255)),
                ('timestart', models.TimeField(max_length=255)),
                ('year', models.IntegerField()),
                ('brigade', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.brigade')),
            ],
        ),
        migrations.CreateModel(
            name='RelutsInsepctions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.report')),
            ],
        ),
        migrations.AddField(
            model_name='brigade',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.cars'),
        ),
        migrations.AddField(
            model_name='brigade',
            name='driver',
            field=models.ForeignKey(limit_choices_to={'status': 'водитель'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='driver_brigades', to='myapp.workers'),
        ),
        migrations.AddField(
            model_name='brigade',
            name='feldsher',
            field=models.ForeignKey(limit_choices_to={'status': 'фельдшер'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='feldsher_brigades', to='myapp.workers'),
        ),
        migrations.AddField(
            model_name='brigade',
            name='med',
            field=models.ForeignKey(limit_choices_to={'status': 'медсестра'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='med_brigades', to='myapp.workers'),
        ),
    ]
