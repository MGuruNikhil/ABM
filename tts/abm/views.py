import requests
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if request.method == "POST":
        text = request.POST["book"]

        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/Yko7PKHZNXotIFUBG7I9"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": "3db03cfcd354d51ed0ae1834c51cefcd"
        }

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
            response['Content-Disposition'] = 'attachment; filename=output.mp3'
            return response

    return render(request, "abm/index.html")