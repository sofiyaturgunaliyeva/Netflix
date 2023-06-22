# Generated by Django 4.2 on 2023-06-22 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aktyor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ism', models.CharField(max_length=50)),
                ('davlat', models.CharField(max_length=50)),
                ('tugilgan_yili', models.CharField(max_length=50)),
                ('jins', models.CharField(choices=[('Ayol', 'Ayol'), ('Erkak', 'Erkak')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Kino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=70)),
                ('janr', models.CharField(max_length=30)),
                ('yil', models.DateField()),
                ('davomiylik', models.DurationField()),
                ('reyting', models.FloatField()),
                ('aktyorlar', models.ManyToManyField(to='app1.aktyor')),
            ],
        ),
        migrations.CreateModel(
            name='Izoh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matn', models.TextField()),
                ('sana', models.DateField(auto_now_add=True)),
                ('baho', models.PositiveSmallIntegerField()),
                ('kino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.kino')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]