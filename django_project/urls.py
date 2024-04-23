from django.conf import settings
from django.conf.urls.static import static
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
    path('text',include('text_convert.urls')),
]+ static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
