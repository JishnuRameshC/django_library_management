from django import forms
from .models import Book,Review,Request

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price','category', 'cover', 'book_pdf_file']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = []
