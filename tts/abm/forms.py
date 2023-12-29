from django import forms

class BookUploadForm(forms.Form):
    inputText = forms.CharField(label="Enter text", required=False)
    book = forms.FileField(
        label="Choose a Book to upload  (supports .pdf, .txt, .html)", 
        required=False
    )
    bookName = forms.CharField(label="Audio Book Name", required=False)