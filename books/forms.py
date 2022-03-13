from django import forms

from .models import Books  

from datetime import datetime
import re


class AddBookForm(forms.ModelForm):
    book_title      = forms.CharField(
                            max_length=150,
                            label='Book title',
                            widget=forms.TextInput(attrs={
                            "placeholder": ""}))

    author          = forms.CharField(
                            max_length=50,
                            label='Author name',
                            widget=forms.TextInput(attrs={
                            "placeholder": "e.g.: J.R.R. Tolkien"}))

    publ_date       = forms.CharField(
                            max_length=10,
                            label='Book publication date',
                            widget=forms.TextInput(attrs={
                            "placeholder": "YYYY-MM-DD"}))

    ISBN_number     = forms.CharField(
                            max_length=13,
                            label='ISBN number',
                            widget=forms.TextInput(attrs={
                            "placeholder": "13-digit ISBN number"}))

    page_count      = forms.IntegerField()

    cover_URL       = forms.URLField(
                            max_length=200,
                            label='Book cover URL',
                            widget=forms.TextInput(attrs={
                            "placeholder": "e.g.: http://google.com"}))

    publ_language   = forms.CharField(
                            max_length=20,
                            label='Publication language',
                            widget=forms.TextInput(attrs={
                            "placeholder": "e.g.: english"}))


    class Meta:
        model = Books
        fields = [
            'book_title',
            'author',
            'publ_date',
            'ISBN_number',
            'page_count',
            'cover_URL',
            'publ_language'
        ]


    # Cleaning method to check if the date is of correct format and
    # not later than today (you cannot have book published in future :))    
    def clean_publ_date(self, *args, **kwargs):
        publ_date = self.cleaned_data.get("publ_date")

        # Date format verification
        date_pattern = '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
        if not re.match(date_pattern, publ_date):
            raise forms.ValidationError(
                'Date should be of "YYYY-MM-DD" format',
                code='invalid'
                )

        # Future date verification
        if datetime.strptime(publ_date, '%Y-%m-%d') > datetime.now():
            raise forms.ValidationError(
                'Date cannot be older than today!',
                code='invalid'
                )
        return publ_date


    # Cleaning method for ensuring, that ISBN number is  of 13 digits
    def clean_ISBN_number(self, *args, **kwargs):
        ISBN_number = self.cleaned_data.get("ISBN_number")
        if len(ISBN_number) < 13:
            raise forms.ValidationError(
                'ISBN number must have 13 digits!',
                code='invalid'
                )
        else:
            return ISBN_number