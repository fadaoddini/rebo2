# Generated by Django 5.1 on 2024-09-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0049_alter_myuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_profile/93a7c2e1-dbbc-473c-be84-2ab4478572c8/'),
        ),
    ]
