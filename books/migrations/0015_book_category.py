# Generated by Django 5.0.4 on 2024-04-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_request_is_returned_request_request_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Biography', 'Biography'), ('History', 'History'), ('Autobiography', 'Autobiography'), ('Education', 'Education'), ('Arts', 'Arts'), ('Photography', 'Photography'), ('Economics', 'Economics'), ('Management', 'Management'), ('Law', 'Law'), ('Health', 'Health'), ('Fiction', 'Fiction'), ('Business', 'Business'), ('Fantasy', 'Fantasy'), ('Space', 'Space'), ('Philosophy', 'Philosophy')], default='Fiction', max_length=200),
        ),
    ]
