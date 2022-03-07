from django.shortcuts import render, get_object_or_404
from .models import Books


# View for home site
def home_view(request):
    return render(request, 'home.html', {})


# View for book list
def book_list_view(request):
    # Getting all objects from DB
    all_books = Books.objects.all()

    # Passing objects from query to context dict
    context = {
        "all_books": all_books
    }
    return render(request, 'book_list.html', context)


