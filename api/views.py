from django.shortcuts import render
from rest_framework import generics

from books.models import Books
from .serializers import BookSerializer

def book_api_view(generic.ListView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    