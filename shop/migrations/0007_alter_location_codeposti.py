# Generated by Django 3.2 on 2024-02-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20240225_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='codeposti',
            field=models.CharField(max_length=30),
        ),
    ]
