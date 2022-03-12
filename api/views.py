from django.shortcuts import render
from rest_framework import generics
from books.models import Books
from .serializers import BookSerializer
from bookshelf.settings import BOOKS_API_KEY
import requests
import re


class BookApiView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer



def api_book_import_view(request):
    context = {}
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

        API_params_dict = {
            'intitle': intitle,
            'inauthor': inauthor,
            'inpublisher': inpublisher,
            'subject': subject,
            'isbn': isbn,
            'lcnn': lcnn,
            'oclc': oclc
        }

        print(API_params_dict.keys(), API_params_dict.values())

        basic_url = f'https://www.googleapis.com/books/v1/volumes?q={keyword}'

        for i in range(0, len(API_params_dict)):
            if list(API_params_dict.values())[i] != '':
                basic_url = basic_url +\
                '+' +\
                str(list(API_params_dict.keys())[i]) +\
                ':' +\
                str(list(API_params_dict.values())[i])


        url = basic_url + f'&key={BOOKS_API_KEY}'
        print(f"YOUR URL: {url}")
        response = requests.get(url)
        data = response.json()
        try:
            books = data['items']

            for book in books:

                try:
                    imported_book_title = book['volumeInfo']['title']
                except KeyError:
                    imported_book_title = None

                try:
                    imported_author = ''
                    multiple_authors = book['volumeInfo']['authors']
                    for author in multiple_authors:
                        if imported_author == '':
                            imported_author = author
                        else:
                            imported_author = imported_author + ', ' + author
                except KeyError:
                    imported_author = None


                try:
                    imported_publ_date = book['volumeInfo']['publishedDate']
                except KeyError:
                    imported_publ_date = None

                year_date_pattern = '^[0-9]{4}$'
                year_month_date_pattern = '^[0-9]{4}-[0-9]{2}$'

                if re.match(year_date_pattern, imported_publ_date):
                    imported_publ_date = imported_publ_date + '-01-01'

                elif re.match(year_month_date_pattern, imported_publ_date):
                    imported_publ_date = imported_publ_date + '-01'

                elif len(imported_publ_date) != 10:
                    imported_publ_date = None


                try:
                    imported_ISBN_number = ''
                    id_numbers_quantity = len(book['volumeInfo']['industryIdentifiers'])
                    for i in range(0, id_numbers_quantity):
                        if book['volumeInfo']['industryIdentifiers'][i]['type'] == 'ISBN_13':
                            imported_ISBN_number = book['volumeInfo']['industryIdentifiers'][i]['identifier']
                except KeyError:
                    imported_ISBN_number = '0' * 13


                try:
                    imported_page_count = book['volumeInfo']['pageCount']
                except KeyError:
                    imported_page_count = None

                try:
                    imported_cover_URL = book['volumeInfo']['imageLinks']['thumbnail']
                except:
                    imported_cover_URL = None

                try:
                    imported_publ_language = book['accessInfo']['country']
                except:
                    imported_publ_language = None

                book_data = Books(
                book_title = imported_book_title,
                author = imported_author,
                publ_date = imported_publ_date,
                ISBN_number = imported_ISBN_number,
                page_count = imported_page_count,
                cover_URL = imported_cover_URL,
                publ_language = imported_publ_language
                )

                book_data.save()
                all_books = Books.objects.all().order_by('-id')
                context = {
                    'all_books': all_books
                }


        except KeyError:
            pass


    return render(request, 'api_book_import.html', context)