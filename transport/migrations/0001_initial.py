# Generated by Django 3.2 on 2024-08-14 22:28

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
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(blank=True, max_length=42, null=True)),
                ('pelak', models.PositiveIntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True)),
                ('status', models.BooleanField(choices=[(True, 'true'), (False, 'false')], default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('expire_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Transport',
                'verbose_name_plural': 'Transports',
            },
        ),
        migrations.CreateModel(
            name='TransportType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/transport/type/')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.CreateModel(
            name='TransportReq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(blank=True, max_length=42, null=True)),
                ('destination', models.CharField(blank=True, max_length=42, null=True)),
                ('distance', models.CharField(blank=True, max_length=42, null=True)),
                ('price', models.PositiveBigIntegerField()),
                ('description', models.TextField(blank=True)),
                ('status', models.BooleanField(choices=[(True, 'true'), (False, 'false')], default=False)),
                ('barnameh', models.CharField(choices=[('ONE_ME', 'one me'), ('UP_TO_YOU', 'up to you')], default='ONE_ME', max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('expire_time', models.DateTimeField(blank=True, null=True)),
                ('my_transport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transport.transport')),
            ],
            options={
                'verbose_name': 'TransportReq',
                'verbose_name_plural': 'TransportReqs',
            },
        ),
        migrations.AddField(
            model_name='transport',
            name='transport_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transport.transporttype'),
        ),
        migrations.AddField(
            model_name='transport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='transports', to=settings.AUTH_USER_MODEL),
        ),
    ]
