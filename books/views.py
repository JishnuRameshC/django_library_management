from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (ListView, DetailView,
                                DeleteView,UpdateView,CreateView)
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.http import FileResponse,HttpResponse
from django.db.models import Q 
from django.core.exceptions import PermissionDenied

from .models import Book,Review,Request,BookPermission
from .forms import BookForm,ReviewForm,RequestForm


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"

class StaffBookListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/libarian/staff_book_list.html"
    permission_required = "books.special_status"

class BookDetailView(
        LoginRequiredMixin,
        # PermissionRequiredMixin,
        DetailView):
    model = Book
    context_object_name = "book"  
    template_name = "books/book_detail.html"
    login_url = "account_login"
    # permission_required = "books.special_status"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()  
        return context


class BookCreateView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        CreateView):
    model = Book
    form_class = BookForm
    login_url = 'account_login'
    permission_required = 'books.can_add_book'
    template_name = 'books/libarian/book_create_form.html'
    success_url = reverse_lazy('book_list')


class BookDeleteView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    login_url = 'account_login'
    permission_required = 'books.can_delete_book'
    template_name = 'books/libarian/book_confirm_delete.html'


class BookUpdateView(LoginRequiredMixin,
        PermissionRequiredMixin,
        UpdateView):
    model = Book
    form_class = BookForm
    login_url = 'account_login'
    permission_required = 'books.can_edit_book'
    template_name = 'books/libarian/book_update_form.html'


# class ReadBookView(DetailView):
#     model = Book
#     template_name = 'books/read_book.html'

#     def get(self, request, *args, **kwargs):
#         book = self.get_object()
#         if book.book_pdf_file:
#             return FileResponse(open(book.book_pdf_file.path, 'rb'), content_type='application/pdf')
#         # Handle case where no PDF is available
#         return HttpResponse("No PDF available for this book.")




class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "books/review_create_form.html"
    login_url = "account_login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.book_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.kwargs["pk"]})
    

class SearchResultsListView(ListView): 
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


class BooksStatusView(LoginRequiredMixin, ListView):
    template_name = 'books/book_status.html'
    context_object_name = 'requested_books'

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)


class BooksStatusStaffView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    template_name = 'books/staff_book_status.html'
    context_object_name = 'book_requests'
    permission_required = 'books.can_view_request'

    
    def get_queryset(self):
        return Request.objects.all()
    

class RequestBookPermissionView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'books/request_permission.html'
    success_url = reverse_lazy('request_confirmation')

    def form_valid(self, form):
        # Check if the user has already made 5 requests
        user_requests_count = Request.objects.filter(user=self.request.user).count()
        if user_requests_count >= 5:
            raise PermissionDenied("You have reached the maximum limit of book requests.")

        # Set default return time to 3 days from the request timestamp
        form.instance.book = Book.objects.get(id=self.kwargs['book_id'])
        form.instance.user = self.request.user
        form.instance.request_timestamp = timezone.now()
        form.instance.return_time = form.instance.request_timestamp + timezone.timedelta(days=3)
        return super().form_valid(form)


class RequestConfirmationView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'books/request_confirmation.html'
    def get_queryset(self):
        return Request.objects.all()

  
class ViewRequestsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'books/view_requests.html'
    model = Request
    context_object_name = 'pending_requests'
    permission_required = 'books.can_view_request'

    def get_queryset(self):
        return Request.objects.all()


class ApproveRequestView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Request
    fields = ['is_approved']
    success_url = reverse_lazy('staff_book_status')
    permission_required = 'books.can_edit_request'

    def form_valid(self, form):
        request_instance = form.instance
        request_instance.is_approved = True
        request_instance.save()
        BookPermission.objects.create(book=request_instance.book, user=request_instance.user, is_approved=True)
        return super().form_valid(form)


class DenyRequestView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Request
    success_url = reverse_lazy('staff_book_status')
    permission_required = 'books.can_edit_request'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)