# Generated by Django 4.0.3 on 2022-03-12 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_books_isbn_number_alter_books_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='publ_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]