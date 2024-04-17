# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
import uuid  # Required for unique book instances
from datetime import date  # noqa

from django.conf import settings
from django.db import models
# from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse  # To generate URLS by reversing URL patterns


# Create your models here.
class MyModelName(models.Model):
    """MyModelName

    Args:
        models (MyModelName): example
    """
    my_field_name = models.CharField(
        max_length=20, help_text='Field documentation')

    class Meta:
        ordering = ['-my_field_name']

    def get_absolute_url(self):
        """get_absolute_url"""
        return reverse("model-detail-view", args=[str(self.id)])

    def __str__(self):
        """STR"""
        return f'{self.my_field_name}'


class Genre(models.Model):
    """Genre

    Args:
        Model representing a book genre
    """
    name = models.CharField(max_length=200, unique=True,
                            help_text='Enter a book genre (e.g. Science Fiction, French Poetry, etc.)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower('name'), name='genre_name_case_insensitive_unique',
                                    violation_error_message="Genre already exists (case insensitive match)"),
        ]


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")

    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    def display_borrower(self):
        """Returns the date of death to access a particular author instance."""
        return self.borrower if self.borrower is not None else "It doesn't have"


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

    def display_date_of_death(self):
        """Returns the date of death to access a particular author instance."""
        return self.date_of_death if self.date_of_death is not None else 'Still alive'

    def get_author_books(self):
        """Returns the Author's books."""
        books = Book.objects.filter(author=self)
        return books


# Language model — challenge
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            ),
        ]
