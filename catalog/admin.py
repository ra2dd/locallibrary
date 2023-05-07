from django.contrib import admin

# Register your models here.
from .models import Genre, Language, Book, Imprint, BookInstance, Author

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Imprint)

# Inline Book for editing it inside Author detail view
class BookInline(admin.StackedInline):
    model = Book
    readonly_fields = ['isbn']

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # Display in list view
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    
    # Display in detail view
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Inline BookInstance for editing it inside Book detail view
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    # book field is excluded automatically because it goes inline to book model with relationship
    fields = ['book', 'id', 'imprint', 'status', 'due_back',]

# Register the Admin classes for Book using the decorator
# Decorator is the function that is run before the function that you pass to decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Display in list view
    list_display = ('book', 'imprint', 'status', 'due_back', 'borrower')
    list_filter = ('status', 'due_back')

    # Display in detail view
    exclude = ['id']
    fieldsets = (
        (None, 
        {
            'fields': ('book', 'imprint')
        }),
        ('Availability',
        {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )