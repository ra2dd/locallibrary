from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),

    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # Achieving the same thing with regular expressions
    # Learn more at https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views#url_mapping_2
    # re_path(r'^book/(?P<pk>\d+)$'views.BookDetailView.as_view(), name='book-detail'),
    
    path('authors/', views.AuthorListView.as_view(), name='authors'),
]