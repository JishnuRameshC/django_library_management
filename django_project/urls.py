from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # user management
    path("accounts/", include("allauth.urls")),
    # local apps
    path('',include('pages.urls')),
    path('book',include('books.urls')),
]
