# Generated by Django 3.2 on 2024-08-12 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_location_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_send',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]