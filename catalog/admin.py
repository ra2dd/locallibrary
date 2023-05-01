from django.contrib import admin

# Register your models here.
from .models import Genre, Language, Book, Imprint, BookInstance, Author

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Imprint)
admin.site.register(BookInstance)
admin.site.register(Author)