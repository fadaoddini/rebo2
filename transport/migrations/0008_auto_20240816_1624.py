# Generated by Django 3.2 on 2024-08-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0007_auto_20240816_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routemetrics',
            name='distance_km',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='routemetrics',
            name='max_cost',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='routemetrics',
            name='max_duration_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='routemetrics',
            name='min_cost',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='routemetrics',
            name='min_duration_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
