# Imports for API View
from rest_framework import generics, filters
from books.models import Books
from .serializers import BookSerializer

# Imports for Google Books API Import
from django.shortcuts import render
from bookshelf.settings import BOOKS_API_KEY
import requests
import re


# REST API Class for generating API view from Django app DB
class BookApiView(generics.ListAPIView):
    # Search and filtering 
    search_fields = [
        'book_title',
        'author',
        'publ_date',
        'ISBN_number'
        ]
    filter_backends = (filters.SearchFilter,)

    # API View
    queryset = Books.objects.all()
    serializer_class = BookSerializer



def api_book_import_view(request):
    context = {}
    imported_books_list = []
    if 'q' in request.GET:

        # API keyword and searching terms
        keyword = request.GET['q']
        intitle = request.GET['intitle']
        inauthor = request.GET['inauthor']
        inpublisher = request.GET['inpublisher']
        subject = request.GET['subject']
        isbn = request.GET['isbn']
        lcnn = request.GET['lcnn']
        oclc = request.GET['oclc']

        # Creating dict with searching terms for requests URL generation
        API_params_dict = {
            'intitle': intitle,
            'inauthor': inauthor,
            'inpublisher': inpublisher,
            'subject': subject,
            'isbn': isbn,
            'lcnn': lcnn,
            'oclc': oclc
        }

        # Base URL for requests library - Google Books API link with searching keyword added
        basic_url = f'https://www.googleapis.com/books/v1/volumes?q={keyword}'

        # Loop for concatenating searching terms to base URL (from API_params_dict)
        for i in range(0, len(API_params_dict)):
            if list(API_params_dict.values())[i] != '':
                basic_url = basic_url +\
                '+' +\
                str(list(API_params_dict.keys())[i]) +\
                ':' +\
                str(list(API_params_dict.values())[i])

        # Concatenating URL modified with searching terms and API Key
        url = basic_url + f'&key={BOOKS_API_KEY}'

        # Getting requests response and converting it to .json file
        response = requests.get(url)
        data = response.json()

        '''
        Longer instructions for picking specific API .json fields matching Django 
        Books Model.
        Each matching .json object is verified:
        - try...except... block for every model field verifying KeyError: it verifies
        whether that record exists in .json file (in Google Books API). If value does
        not exist - it is assigned with "None" value;
        - depending on model field - every value (if exists) is cleaned to match each
        model field (e.g.: if publication date in .json has only year, it has automatically
        added '-01-01' to be compatible with ModelForm date format: YYYY-MM-DD)
        '''
        try:
            books = data['items']

            for book in books:

                # Checking whether the book title exists in book .json
                try:
                    imported_book_title = book['volumeInfo']['title']
                except KeyError:
                    imported_book_title = None

                # Checking whether the author name exists in book .json
                try:
                    imported_author = ''
                    multiple_authors = book['volumeInfo']['authors']
                    # Concatenating list of more than 1 author into string
                    for author in multiple_authors:
                        if imported_author == '':
                            imported_author = author
                        else:
                            imported_author = imported_author + ', ' + author
                except KeyError:
                    imported_author = None

                # Checking whether the publication date exists in book .json
                try:
                    imported_publ_date = book['volumeInfo']['publishedDate']
                except KeyError:
                    imported_publ_date = None

                # Repairing dates consisting only of year or year and month to YYYY-MM-DD format
                year_date_pattern = '^[0-9]{4}$'
                year_month_date_pattern = '^[0-9]{4}-[0-9]{2}$'

                if re.match(year_date_pattern, imported_publ_date):
                    imported_publ_date = imported_publ_date + '-01-01'

                elif re.match(year_month_date_pattern, imported_publ_date):
                    imported_publ_date = imported_publ_date + '-01'

                # If date other than YYYY. YYYY-MM or YYYY-MM-DD - assign 'None' to model field
                elif len(imported_publ_date) != 10:
                    imported_publ_date = None

                # Checking whether the ISBN number exists in book .json
                try:
                    imported_ISBN_number = ''
                    # If more than one book identify numbers (e.g.: ISBN_10) - pick the right one (ISBN_13)
                    id_numbers_quantity = len(book['volumeInfo']['industryIdentifiers'])
                    for i in range(0, id_numbers_quantity):
                        if book['volumeInfo']['industryIdentifiers'][i]['type'] == 'ISBN_13':
                            imported_ISBN_number = book['volumeInfo']['industryIdentifiers'][i]['identifier']
                except KeyError:
                    imported_ISBN_number = '0' * 13

                # Checking whether the page count exists in book .json
                try:
                    imported_page_count = book['volumeInfo']['pageCount']
                except KeyError:
                    imported_page_count = None

                # Checking whether the cover URL exists in book .json
                try:
                    imported_cover_URL = book['volumeInfo']['imageLinks']['thumbnail']
                except:
                    imported_cover_URL = None

                # Checking whether the publication language exists in book .json
                try:
                    imported_publ_language = book['accessInfo']['country']
                except:
                    imported_publ_language = None

                # Assign cleaned data to responding model fields
                book_data = Books(
                book_title = imported_book_title,
                author = imported_author,
                publ_date = imported_publ_date,
                ISBN_number = imported_ISBN_number,
                page_count = imported_page_count,
                cover_URL = imported_cover_URL,
                publ_language = imported_publ_language
                )

                imported_books_list.append(book_data)
                book_data.save() # Add object to database
                all_books = Books.objects.all().order_by('-id') # 
                context = {
                    'all_books': all_books,
                    'imported_books_list': imported_books_list
                }


        except KeyError:
            # Empty response in case of other request or not matching search keyword to API records
            pass


    return render(request, 'api_book_import.html', context)