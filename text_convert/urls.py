from django.urls import path
from .views import PDFToTextFormView,PDFTextDisplayView,ConvertTextToSpeechView,download_audio

urlpatterns = [
    path('', PDFToTextFormView.as_view(), name='pdf_to_text'),
    path('result/', PDFTextDisplayView.as_view(), name='pdf_to_text_result'),
    path('text_to_speech/', ConvertTextToSpeechView.as_view(), name='text_to_speech'),
    path('download/', download_audio, name='download_audio'),
]
