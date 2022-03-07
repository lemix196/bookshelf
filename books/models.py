from django.db import models

# Create your models here.

class Books(models.Model):
    book_title      = models.CharField(max_length=150)
    author          = models.CharField(max_length=50)
    publ_date       = models.CharField(max_length=10)
    ISBN_number     = models.CharField(max_length=13)
    page_count      = models.PositiveIntegerField()
    cover_URL       = models.URLField(max_length=200)
    publ_language   = models.CharField(max_length=20)


    class Meta:
        verbose_name_plural = "Books"