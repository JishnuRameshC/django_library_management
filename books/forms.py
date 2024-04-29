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


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    format = "%Y-%m-%dT%H:%M"  # Format for input field value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class RequestForm(forms.ModelForm):
    return_time = forms.DateTimeField(widget=DateTimeInput())

    class Meta:
        model = Request
        fields = ['return_time'] 
