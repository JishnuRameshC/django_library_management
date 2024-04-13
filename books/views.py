from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                DeleteView,UpdateView,CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from .models import Book,Review
from .forms import BookForm,ReviewForm


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
    permission_required = 'books.delete_book'
    template_name = 'books/book_confirm_delete.html'


class BookUpdateView(LoginRequiredMixin,
        PermissionRequiredMixin,
        UpdateView):
    model = Book
    form_class = BookForm
    login_url = 'account_login'
    permission_required = 'books.change_book'
    template_name = 'books/book_update_form.html'


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