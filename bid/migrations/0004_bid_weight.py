# Generated by Django 3.2 on 2024-09-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0003_bid_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='weight',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]