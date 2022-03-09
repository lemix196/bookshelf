from django.shortcuts import render
from rest_framework import generics

from books.models import Books
from .serializers import BookSerializer

class BookApiView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
