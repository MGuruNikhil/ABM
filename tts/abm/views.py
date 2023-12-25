import requests
from django.shortcuts import render
from django.http import HttpResponse
from .forms import BookUploadForm
import PyPDF2
from ebooklib import epub
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


def extractTextFromEpub(filePath):
    file = filePath.read()
    epubBook = epub.read_epub(file)
    text = ' '.join(item.get_content().decode('utf-8') for item in epubBook.get_items_of_type('text'))
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
            book = request.FILES['book']

            bookName = form.cleaned_data.get('bookName', 'output.mp3')
            if bookName[-4:] != ".mp3":
                bookName += ".mp3"

            bookExtension = book.name.split('.')[-1].lower()

            if bookExtension == 'pdf':
                text = extractTextFromPdf(book)
            elif bookExtension == 'epub':
                text = extractTextFromEpub(book)
            elif bookExtension == 'txt':
                text = extractTextFromTxt(book)
            elif bookExtension == 'html':
                text = extractTextFromHtml(book)
            else:
                text = "Unsupported file type"

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
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        response.write(chunk)
                return response
    else:
        form = BookUploadForm()

    return render(request, "abm/index.html", {'form': form})