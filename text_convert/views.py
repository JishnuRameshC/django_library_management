
import requests
import base64
from django.shortcuts import render
from django.views.generic import FormView
from django.http import FileResponse,HttpResponse
from django.urls import reverse_lazy

from .forms import TextToSpeechForm, PDFUploadForm,TextInputForm

from PyPDF2 import PdfReader


class ConvertTextToSpeechView(FormView):
    template_name = 'text_convert/text_to_speech.html'
    form_class = TextToSpeechForm
    success_url = reverse_lazy('download_audio')

    def form_valid(self, form):
        text_to_convert = form.cleaned_data['text']
        
        # API endpoint URL
        url = "https://joj-text-to-speech.p.rapidapi.com/"
        
        # Payload containing text, voice settings, and audio configuration
        payload = {
            "input": {"text": text_to_convert},
            "voice": {
                "languageCode": "en-US",
                "name": "en-US-News-L",
                "ssmlGender": "FEMALE"
            },
            "audioConfig": {"audioEncoding": "MP3"}
        }
        
        # Headers including RapidAPI key and host
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "api_kery_here",
            "X-RapidAPI-Host": "joj-text-to-speech.p.rapidapi.com"
        }
        
        # Sending POST request to the API
        response = requests.post(url, json=payload, headers=headers)
        
        # Checking response status
        if response.status_code == 200:
            # Decoding base64 audio content
            audio_content = base64.b64decode(response.json()['audioContent'])
            
            # Saving the audio content to a temporary file
            with open("output.mp3", "wb") as audio_file:
                audio_file.write(audio_content)
        
        return super().form_valid(form)

def download_audio(request):
    with open("output.mp3", "rb") as audio_file:
        response = HttpResponse(audio_file.read(), content_type="audio/mpeg")
        response['Content-Disposition'] = 'attachment; filename="output.mp3"'
        return response


class PDFToTextFormView(FormView):
    template_name = 'text_convert/upload_pdf.html'
    form_class = PDFUploadForm

    def form_valid(self, form):
        pdf_file = form.cleaned_data['pdf_file']
        text = self.convert_pdf_to_text(pdf_file)
        return render(self.request, 'text_convert/pdf_text_display.html', {'text': text})

    def convert_pdf_to_text(self, pdf_file):
        try:
            reader = PdfReader(pdf_file)
            number_of_pages = len(reader.pages)
            text = ""
            for page_num in range(number_of_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error converting PDF to text: {str(e)}"


class PDFTextDisplayView(FormView):
    template_name = 'text_convert/pdf_text_display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extracted_text'] = self.request.session.get('extracted_text', '')
        return context
    


# class MyFormView(FormView):
#     template_name = 'my_template.html'
#     form_class = TextInputForm
#     success_url = '/success/'  

#     def form_valid(self, form):
#         text = form.cleaned_data['text']
        
#         # Convert text to speech using gTTS
#         tts = gTTS(text=text, lang='en')
        
#         # Save the audio file temporarily
#         audio_file_path = '/tmp/output.mp3'
#         tts.save(audio_file_path)
        
#         # Return the audio file as response
#         return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')