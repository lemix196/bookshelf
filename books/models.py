from django.db import models

# Create your models here.

class Books(models.Model):
    book_title      = models.CharField(max_length=150, blank=True, null=True)
    author          = models.CharField(max_length=200, blank=True, null=True)
    publ_date       = models.DateField(auto_now=False, blank=True, null=True)
    ISBN_number     = models.CharField(max_length=13, blank=True, null=True)
    page_count      = models.PositiveIntegerField(blank=True, null=True)
    cover_URL       = models.URLField(max_length=200, blank=True, null=True)
    publ_language   = models.CharField(max_length=20, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Books"
