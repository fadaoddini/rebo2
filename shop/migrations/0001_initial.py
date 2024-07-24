# Generated by Django 3.2 on 2024-02-23 11:49

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
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_brand_shop', to='shop.brand')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_category_shop', to='shop.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.BigIntegerField(unique=True)),
                ('price', models.PositiveBigIntegerField()),
                ('discount', models.PositiveIntegerField(default=0)),
                ('weight', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True)),
                ('warranty', models.BooleanField(choices=[(True, 'true'), (False, 'false')], default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('number_exist', models.PositiveIntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.category')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='products_shop', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='shop/rebo/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_shop', to='shop.product')),
            ],
        ),
    ]
