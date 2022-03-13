from django.test import TestCase
from books.models import Books 

class BooksTestCase(TestCase):
    def setUp(self):
        Books.objects.create(
            book_title="Example title",
            author="Thomas Author",
            publ_date="2022-01-01",
            ISBN_number="1234123412342",
            page_count=100,
            cover_URL="https://google.com",
            publ_language="PL"
            )

    def tearDown(self):
        obj = Books.objects.get(book_title="Example title")
        obj.delete()


    def test_book_title_max_length(self):
        book = Books.objects.get(id=1)
        max_length = book._meta.get_field('book_title').max_length
        self.assertEqual(max_length, 150)


    def test_author_max_length(self):
        book = Books.objects.get(id=1)
        max_length = book._meta.get_field('author').max_length
        self.assertEqual(max_length, 200)


    def test_ISBN_number_max_length(self):
        book = Books.objects.get(id=1)
        max_length = book._meta.get_field('ISBN_number').max_length
        self.assertEqual(max_length, 13)


    def test_cover_URL_max_length(self):
        book = Books.objects.get(id=1)
        max_length = book._meta.get_field('cover_URL').max_length
        self.assertEqual(max_length, 200)


    def test_publ_language_max_length(self):
        book = Books.objects.get(id=1)
        max_length = book._meta.get_field('publ_language').max_length
        self.assertEqual(max_length, 20)



