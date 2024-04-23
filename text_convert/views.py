from django.shortcuts import render
from django.views.generic import FormView
from django.http import FileResponse

from .forms import PDFUploadForm,TextInputForm

from PyPDF2 import PdfReader





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