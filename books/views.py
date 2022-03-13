from django.shortcuts import render, get_object_or_404
from .models import Books
from .forms import AddBookForm


# View for home site
def home_view(request):
    return render(request, 'home.html', {})


# View for book list
def book_list_view(request):
    # Getting all objects from DB
    all_books = Books.objects.all()
    model_fields = Books._meta.get_fields()
    # Passing objects from query to context dict
    context = {
        "all_books": all_books,
        "model_fields": model_fields
    }
    return render(request, 'book_list.html', context)


# View for searching books
def book_search_view(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        if request.POST['search_by'] != 'publ_date':
            search_by = request.POST['search_by'] + "__contains"
            searched_books = Books.objects.filter(**{ search_by: searched })

        else:
            search_by = request.POST['search_by']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']

            print(date_from, date_to)

            searched_books = Books.objects.filter(publ_date__range=[date_from, date_to])

        context = {
            'searched': searched,
            'search_by': search_by,
            'searched_books': searched_books
        }

        return render(request, 'book_search.html', context)

    else:


        context = {

        }

        return render(request, 'book_search.html', context)


# View for adding book
def book_add_view(request):
    form = AddBookForm(request.POST or None)
    if form.is_valid() and form:
        form.save()
        form = AddBookForm()

    context = {
        'form': form
    }

    return render(request, 'book_add.html', context)


