# Generated by Django 4.0.3 on 2022-03-09 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_books_publ_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='publ_date',
            field=models.DateField(auto_now=True),
        ),
    ]
