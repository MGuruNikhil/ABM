from django import forms

class BookUploadForm(forms.Form):
    book = forms.FileField(
        label="Choose a Book to upload",
    )
    bookName = forms.CharField(label="Audio Book Name", required=False)