from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')

class TextInputForm(forms.Form):
    pdf_file = forms.Textarea()
    

class TextToSpeechForm(forms.Form):
    text = forms.CharField(label='Enter Text', max_length=1000, widget=forms.Textarea)


