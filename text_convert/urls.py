from django.urls import path
from .views import PDFToTextFormView,PDFTextDisplayView

urlpatterns = [
    path('', PDFToTextFormView.as_view(), name='pdf_to_text'),
    path('result/', PDFTextDisplayView.as_view(), name='pdf_to_text_result'),
]
