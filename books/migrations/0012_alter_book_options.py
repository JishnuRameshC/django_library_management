# Generated by Django 5.0.4 on 2024-04-19 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_book_cover'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('special_status', 'Can read all books'), ('can_view_book', 'Can view book'), ('can_edit_book', 'Can edit book'), ('can_delete_book', 'Can delete book'), ('can_add_book', 'Can add book')]},
        ),
    ]
