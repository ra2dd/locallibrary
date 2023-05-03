from django.shortcuts import render
from django.views import generic
from .models import Author, Book, BookInstance, Genre

def index(request):
    """View function for home page of the site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    
    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Books that are written in english
    english_books = Book.objects.filter(language__name__icontains='english').count()
    
    indexContext = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'english_books': english_books
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=indexContext)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list' # can change a name for the list to access in a template variable
    # queryset = Book.objects.filter(language__name__icontains='english')[:3] # get 3 books that were written in english
    # template_name = 'books/specify_your_own_template_name_and_location'

    def get_queryset(self):
        return Book.objects.filter(language__name__icontains='english')[:3]