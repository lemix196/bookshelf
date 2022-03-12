# Generated by Django 4.0.3 on 2022-03-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_books_publ_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='ISBN_number',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_title',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='books',
            name='cover_URL',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='publ_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='publ_language',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
