# Generated by Django 5.1 on 2024-09-03 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_product_is_successful_alter_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]