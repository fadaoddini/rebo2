# Generated by Django 5.1 on 2024-09-02 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_successful',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
