# Generated by Django 5.1 on 2024-09-06 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0047_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/80c4f085-c538-4409-b68f-756a51efb703/'),
        ),
    ]
