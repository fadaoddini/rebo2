# Generated by Django 3.2 on 2024-08-12 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0010_product_number_send'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_shop', models.CharField(max_length=32)),
                ('administrator', models.CharField(max_length=48)),
                ('mobile', models.CharField(max_length=20)),
                ('code_posti', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('image', models.ImageField(upload_to='%Y/%m/%d/myshop/')),
                ('is_active', models.BooleanField(choices=[(True, 'active'), (False, 'inactive')], default=False)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MyShop',
                'verbose_name_plural': 'MyShops',
            },
        ),
        migrations.RenameField(
            model_name='product',
            old_name='warranty',
            new_name='vije',
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.AddField(
            model_name='product',
            name='my_shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shop.myshop'),
            preserve_default=False,
        ),
    ]