# Generated by Django 3.2 on 2024-08-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0008_auto_20240816_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='routemetrics',
            name='transport_capacity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]