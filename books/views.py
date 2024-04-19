from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                DeleteView,UpdateView,CreateView)
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.http import FileResponse,HttpResponse
from django.db.models import Q 

from .models import Book,Review,Request,BookPermission
from .forms import BookForm,ReviewForm,RequestForm


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"


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
    permission_required = 'books.add_book'
    template_name = 'books/book_create_form.html'
    success_url = reverse_lazy('book_list')


class BookDeleteView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    login_url = 'account_login'
    permission_required = 'books.can_delete_book'
    template_name = 'books/book_confirm_delete.html'


class BookUpdateView(LoginRequiredMixin,
        PermissionRequiredMixin,
        UpdateView):
    model = Book
    form_class = BookForm
    login_url = 'account_login'
    permission_required = 'books.change_book'
    template_name = 'books/book_update_form.html'

class ReadBookView(DetailView):
    model = Book
    template_name = 'books/read_book.html'

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        if book.book_pdf_file:
            return FileResponse(open(book.book_pdf_file.path, 'rb'), content_type='application/pdf')
        # Handle case where no PDF is available
        return HttpResponse("No PDF available for this book.")

# class PDFDetailView(DetailView):
#     model = Book
#     content_type = 'application/pdf'

#     def render_to_response(self, context, **response_kwargs):
#         pdf_doc = self.get_object()
#         return FileResponse(open(pdf_doc.pdf_file.path, 'rb'), content_type=self.content_type)


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


class BooksStatusStaffView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    template_name = 'books/staff_book_status.html'
    context_object_name = 'book_requests'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        return Request.objects.all()
    

class RequestBookPermissionView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'books/request_permission.html'
    success_url = reverse_lazy('request_confirmation')

    def form_valid(self, form):
        form.instance.book = Book.objects.get(id=self.kwargs['book_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)


class RequestConfirmationView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'books/request_confirmation.html'
    def get_queryset(self):
        return Request.objects.all()

  
class ViewRequestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'books/view_requests.html'
    model = Request
    context_object_name = 'pending_requests'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Request.objects.all()


class ApproveRequestView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Request
    fields = ['is_approved']
    success_url = reverse_lazy('staff_book_status')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        request_instance = form.instance
        request_instance.is_approved = True
        request_instance.save()
        BookPermission.objects.create(book=request_instance.book, user=request_instance.user, is_approved=True)
        return super().form_valid(form)

class DenyRequestView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Request
    success_url = reverse_lazy('view_requests')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)