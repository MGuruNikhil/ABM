import requests
from django.shortcuts import render
from django.http import HttpResponse
from .forms import BookUploadForm
import PyPDF2
from bs4 import BeautifulSoup

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/Yko7PKHZNXotIFUBG7I9"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "3db03cfcd354d51ed0ae1834c51cefcd"
}

def extractTextFromPdf(filePath):
    pdfReader = PyPDF2.PdfReader(filePath)
    text = ''
    for pageNum in range(len(pdfReader.pages)):
        page = pdfReader.pages[pageNum]
        text += page.extract_text()
    return text

def extractTextFromTxt(filePath):
    text = filePath.read().decode('utf-8')
    return text

def extractTextFromHtml(filePath):
    file = filePath.read().decode('utf-8')
    soup = BeautifulSoup(file, 'html.parser')
    text = soup.get_text()
    return text

def index(request):
    if request.method == "POST":
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            inputText = form.cleaned_data.get('inputText')

            bookName = form.cleaned_data.get('bookName', 'output.mp3')
            if bookName[-4:] != ".mp3":
                bookName += ".mp3"

            if not inputText:

                book = request.FILES['book']

                bookExtension = book.name.split('.')[-1].lower()

                if bookExtension == 'pdf':
                    text = extractTextFromPdf(book)
                elif bookExtension == 'txt':
                    text = extractTextFromTxt(book)
                elif bookExtension == 'html':
                    text = extractTextFromHtml(book)
                else:
                    text = "Unsupported file type"
            else:
                text = inputText

            if len(text) <= 2500:
                data = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }

                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    response = HttpResponse(response.content, content_type='audio/mp3')
                    response['Content-Disposition'] = f'attachment; filename="{ bookName }"'
                    return response
    else:
        form = BookUploadForm()

    return render(request, "abm/index.html", {'form': form})