import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Author, Book, BookInstance, Genre
from catalog.forms import RenewBookForm
from .scripts import *

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


    # Number of vistis to this view, counted in the session variable.
       
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    

    indexContext = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'english_books': english_books,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=indexContext)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list' # can change a name for the list to access in a template variable
    paginate_by = 10
    # queryset = Book.objects.filter(language__name__icontains='english')[:3] # get 3 books that were written in english
    # template_name = 'books/specify_your_own_template_name_and_location'

    """
    def get_queryset(self):
        return Book.objects.filter(language__name__icontains='english')[:3]
    """
    
class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = 'catalog/bookinstance_list_user_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return(
            BookInstance.objects
            .filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
   
class AllBooksBorrowedListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all the books that have been borrowed."""
    model = BookInstance
    template_name = 'catalog/bookinstance_all_borrowed_books.html'

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return(
            BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back')
        )

# Decorators for required login and permission    
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian"""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request than process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with the data form the request (binding)
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            # Process the data in form.clened_data as required
            # Here we write the data to the model due_back field
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Redirect to a new URL
            return HttpResponseRedirect(reverse('all-borrowed'))
    
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': datetime.date.today()}

    permission_required = 'catalog.can_modify_book_data'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Not recommended (Potential security issue if more fields added)

    permission_required = 'catalog.can_modify_book_data'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    permission_required = 'catalog.can_modify_book_data'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

    permission_required = 'catalog.can_modify_book_data'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

    permission_required = 'catalog.can_modify_book_data'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')

    permission_required = 'catalog.can_modify_book_data'
