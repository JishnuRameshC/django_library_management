import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .models import Book, Review,Request

class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser1@email.com",
            password="testpass123"
        )

        cls.user.user_permissions.add(
            Permission.objects.get(codename="can_view_book"),
            Permission.objects.get(codename="can_delete_book"),
            Permission.objects.get(codename="special_status"),
            Permission.objects.get(codename="can_add_book"),
            Permission.objects.get(codename="can_edit_book"),
            Permission.objects.get(codename="can_view_request"),
            Permission.objects.get(codename="can_delete_request"),
            Permission.objects.get(codename="can_add_request"),
            Permission.objects.get(codename="can_edit_request"),
        )

        cls.book = Book.objects.create(
            title="Harry Potter",
            author="JK Rowling",
            price="25.00",
        )

        cls.review = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review="An excellent review",
        )

        cls.request_instance = Request.objects.create(
            book=cls.book,
            user=cls.user
        )

    def test_book_listing(self):
        self.assertEqual(f"{self.book.title}", "Harry Potter")
        self.assertEqual(f"{self.book.author}", "JK Rowling")
        self.assertEqual(f"{self.book.price}", "25.00")

    def test_book_list_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_detail_view(self): 
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "books/book_detail.html")

    def test_book_create_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.post(reverse("book_create"), {
            "title": "New Book",
            "author": "New Author",
            "price": "30.00",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_book_update_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.post(reverse("book_update", kwargs={"pk": self.book.pk}), {
            "title": "Updated Title",
            "author": "Updated Author",
            "price": "400",
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")
        self.assertEqual(self.book.author, "Updated Author")
        self.assertEqual(self.book.price, 400.00)

    def test_book_delete_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.post(reverse("book_delete", kwargs={"pk": self.book.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(title="Harry Potter").exists())

    def test_review_create_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.post(reverse("review_create", kwargs={"pk": self.book.pk}), {
            "review": "A new review",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(review="A new review").exists())

    def test_search_results_view(self):
        response = self.client.get(reverse("search_results") + "?q=Harry")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/search_results.html")

    def test_books_status_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.get(reverse("book_status"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_status.html")

    def test_books_status_staff_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.get(reverse("staff_book_status"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/staff_book_status.html")

    def test_request_permission_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.get(reverse("request_permission", kwargs={"book_id": self.book.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/request_permission.html")

    def test_view_requests_view(self):
        self.client.login(email="reviewuser1@email.com", password="testpass123")
        response = self.client.get(reverse("view_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/view_requests.html")

    def test_approve_request_view(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(reverse("approve_request", kwargs={"pk": self.request_instance.pk}))
        self.assertEqual(response.status_code, 302)

    def test_deny_request_view(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(reverse("deny_request", kwargs={"pk": self.request_instance.pk}))
        self.assertEqual(response.status_code, 302)
