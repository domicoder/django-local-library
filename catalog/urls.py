# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
from django.urls import path  # noqa

from . import views  # noqa

urlpatterns = [
    # home page
    path('', views.index, name='index'),

    # Books
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    # Authors
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    # On loan books to User
    path('my-books/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    # On loan books from all Users
    path('borrowed/', views.LoanedBooksFromAllUsersListView.as_view(),
         name='all-borrowed'),
]
