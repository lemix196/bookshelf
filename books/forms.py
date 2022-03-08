form django import forms

from .models import Books  


class AddBook(forms.ModelForm):
    book_title      = forms.CharField(max_length=150)
    author          = forms.CharField(max_length=50)
    publ_date       = forms.CharField(max_length=10)
    ISBN_number     = forms.CharField(max_length=13)
    page_count      = forms.IntegerField()
    cover_URL       = forms.URLField(max_length=200)
    publ_language   = forms.CharField(max_length=20)