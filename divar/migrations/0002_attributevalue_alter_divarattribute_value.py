# Generated by Django 5.1 on 2024-08-28 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='divar.attribute')),
            ],
        ),
        migrations.AlterField(
            model_name='divarattribute',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='divar.attributevalue'),
        ),
    ]