from django.urls import path

from .views import (
    BookListView, 
    BookDetailView,
    BookCreateView,
    BookDeleteView,
    BookUpdateView,
    ReadBookView,
    BooksStatusView,
    ReviewCreateView,
    SearchResultsListView,
    RequestBookPermissionView,
    RequestConfirmationView,
    ViewRequestsView,
    ApproveRequestView,
    DenyRequestView,
    BooksStatusStaffView,
    )


urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<uuid:pk>/review/create/', ReviewCreateView.as_view(), name='review_create'),
    path('status/',BooksStatusView.as_view(), name='book_status'),
    
    # URLs for book management accessible to staff only
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('<uuid:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<uuid:pk>/update/', BookUpdateView.as_view(), name='book_update'),

    # URLs for request permission
    path('request-permission/<uuid:book_id>/', RequestBookPermissionView.as_view(), name='request_permission'),
    path('request-confirmation/', RequestConfirmationView.as_view(), name='request_confirmation'),

    # URLs for staff only
    path('view-requests/', ViewRequestsView.as_view(), name='view_requests'),
    path('approve-request/<int:pk>/', ApproveRequestView.as_view(), name='approve_request'),
    path('deny-request/<int:pk>/', DenyRequestView.as_view(), name='deny_request'),
    path('staff-status/', BooksStatusStaffView.as_view(), name='staff_book_status'),
    path('read/<uuid:pk>/', ReadBookView.as_view(), name='read_book'),
]
