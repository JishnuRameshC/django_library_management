import uuid  
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

def default_cover_image():
    return "covers/default_cover.jpg"


class Book(models.Model):
    categories_list = [("Biography", "Biography"),("History", "History"), ("Autobiography", "Autobiography"), ("Education","Education"),
                       ("Arts","Arts"), ("Photography","Photography"),("Economics","Economics"), ("Management","Management"),("Law","Law"),
                       ("Health","Health"),("Fiction","Fiction"),("Business","Business"),("Fantasy" ,"Fantasy"),("Space","Space"),
                       ("Philosophy","Philosophy")]
    id = models.UUIDField( 
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(choices=categories_list, default="Fiction", max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to="covers/", default=default_cover_image)
    book_pdf_file = models.FileField(upload_to='pdfs/', blank=True)

    class Meta:
        permissions = [
            ("special_status", "Can read all books"),
            ("can_view_book", "Can view book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
            ("can_add_book", "Can add book"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class BookPermission(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="book_permissions"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="book_permissions"
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Request(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    is_approved = models.BooleanField(default=None, null=True)
    request_timestamp = models.DateTimeField(default=timezone.now)
    is_returned = models.BooleanField(default=False)
    return_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        permissions = [
            ("can_view_request", "Can view request"),
            ("can_edit_request", "Can edit request"),
            ("can_delete_request", "Can delete request"),
            ("can_add_request", "Can add request"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Review(models.Model):  
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review