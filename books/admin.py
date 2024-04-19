from django.contrib import admin
from .models import Book, Review,BookPermission,Request


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ("title", "author", "price",)


admin.site.register(Book, BookAdmin)
admin.site.register(BookPermission)
admin.site.register(Request)