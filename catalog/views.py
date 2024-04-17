# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render  # noqa
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from .models import Author, Book, BookInstance, Genre


@login_required  # restrict access to function-based views
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # Available books (genre = 'Stars')
    num_books_word_stars = Book.objects.filter(
        title__icontains="Stars").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_word_stars': num_books_word_stars,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class CustomLoginView(LoginView):
    """Redirect user to home page if try to go to Login page, if it is authenticated."""
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class BookListView(LoginRequiredMixin, generic.ListView):
    # LoginRequiredMixin: to restrict access to class-based views
    model = Book
    paginate_by = 10
    # your own name for the list as a template variable
    context_object_name = 'book_list'
    template_name = 'catalog/book/book_list.html'
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'catalog/book/book_detail.html'


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'author_list'
    template_name = 'catalog/author/author_list.html'


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'catalog/author/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context['books'] = Book.objects.filter(author=author)
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    context_object_name = 'bookinstance_list'
    template_name = 'catalog/bookinstance/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LoanedBooksFromAllUsersListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to all user."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    context_object_name = 'bookinstance_list'
    template_name = 'catalog/bookinstance/bookinstance_list_borrowed_all_users.html'
    paginate_by = 10

    def get_queryset(self):
        # filter(borrower=self.request.user)
        return (
            BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back')
        )
