# Generated by Django 4.0.3 on 2022-03-09 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_books_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='publ_date',
            field=models.DateField(),
        ),
    ]
