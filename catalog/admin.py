# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
from django.contrib import admin  # noqa

from .models import Author, Book, BookInstance, Genre, Language

# Register your models here.

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

# Inline editing of associated records


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # NO spare book instances by default, without this we'll have 3 placeholder


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

# Register a ModelAdmin class
# We won't change the Language and Genre model presentation
# because they only have one field each, so there is no real benefit in doing so!


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BooksInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id', 'borrower')

    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
