from django.contrib import admin

# Register your models here.
from .models import Genre, Language, Book, Imprint, BookInstance, Author

admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
admin.site.register(Imprint)
# admin.site.register(BookInstance)
# admin.site.register(Author)


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Register the Admin classes for Book using the decorator
# Decorator is the function that is run before the function that you pass to decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'due_back')