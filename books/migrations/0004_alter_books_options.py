# Generated by Django 4.0.3 on 2022-03-07 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_books_publ_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='books',
            options={'verbose_name_plural': 'Books'},
        ),
    ]
