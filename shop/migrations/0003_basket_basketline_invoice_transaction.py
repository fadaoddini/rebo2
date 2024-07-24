# Generated by Django 3.2 on 2024-02-23 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_product_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basket_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='baskets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Basket',
                'verbose_name_plural': 'Baskets',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='baskets_invoice', to='shop.basket')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveBigIntegerField()),
                ('status', models.CharField(choices=[('PENDING', 'pending'), ('FAILED', 'failed'), ('COMPLETE', 'complete')], default='PENDING', max_length=100)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='invoices', to='shop.invoice')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='BasketLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveBigIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('total_price', models.PositiveBigIntegerField()),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='products', to='shop.product')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='baskets_line', to='shop.basket')),
            ],
            options={
                'verbose_name': 'BasketLine',
                'verbose_name_plural': 'BasketLines',
            },
        ),
    ]
