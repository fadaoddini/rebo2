# Generated by Django 3.2 on 2024-08-15 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0002_transport_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='iran',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transportreq',
            name='my_transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transportreqs', to='transport.transport'),
        ),
    ]
