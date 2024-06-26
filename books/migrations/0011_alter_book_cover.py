# Generated by Django 5.0.4 on 2024-04-19 08:11

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_request_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(default=books.models.default_cover_image, upload_to='covers/'),
        ),
    ]
