from django.urls import path

from .views import (BookListView, BookDetailView,BookCreateView,
                    BookDeleteView,BookUpdateView,ReviewCreateView,
                    SearchResultsListView)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<uuid:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<uuid:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<uuid:pk>/review/create/', ReviewCreateView.as_view(), name='review_create'),
    path("search/", SearchResultsListView.as_view(),name="search_results"),
]