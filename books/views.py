from django.shortcuts import render, get_object_or_404, redirect
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

    # Passing objects from query to context dict for template rendering
    context = {
        "all_books": all_books,
        "model_fields": model_fields
        }    
    return render(request, 'book_list.html', context)


# View for searching books
def book_search_view(request):
    if request.method == 'POST':
        
        dates = []

        # Searching by book title, author or isbn number
        if request.POST['search_by'] != 'publ_date':
            searched = request.POST['searched']
            search_by = request.POST['search_by'] + "__contains"
            searched_books = Books.objects.filter(**{ search_by: searched })
            # Saving searching data to dict for template rendering
            context = {
                'searched': searched,
                'search_by': search_by,
                'searched_books': searched_books,
                'dates': dates
                }
        #Searching by date interval
        else:
            search_by = request.POST['search_by']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            dates = [date_from, date_to]
            searched_books = Books.objects.filter(publ_date__range=[date_from, date_to])
            # Saving searching data to dict for template rendering
            context = {
                'search_by': search_by,
                'searched_books': searched_books,
                'dates': dates
                }

        return render(request, 'book_search.html', context)

    # Saving no data if other request method
    else:
        context = {}
        return render(request, 'book_search.html', context)


# View for adding book
def book_add_view(request):
    form = AddBookForm(request.POST or None)
    if form.is_valid() and form:
        form.save()
        form = AddBookForm()

    # Passing form info to dict for template rendering
    context = {
        'form': form
    }

    return render(request, 'book_add.html', context)


# View fo editing book
def book_edit_view(request, book_id):
    obj = get_object_or_404(Books, id=book_id)
    form = AddBookForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }

    return render(request, 'book_add.html', context)

# View for deleting book
def book_delete_view(request, book_id):
    obj = get_object_or_404(Books, id=book_id)

    if request.method == 'POST':
        obj.delete()
        return redirect('book_list/') # Need to change to proper url

    context = {
        'object': obj
    }

    return render(request, 'book_delete.html', context)


