from django.shortcuts import render

# Create your views here.
from testapp.forms import TestForm

import requests
import base64
import io


def TestView(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            eng_text = papago(text)
            make_audio(text)
            # result = dall_e(eng_text)
            return render(request, 'testapp/result.html', {'text': text, 'eng_text': eng_text})  # , 'result': result
    else:
        form = TestForm()
        return render(request, 'testapp/test.html', {'form': form})


def papago(text):
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'X-Naver-Client-Id': 'brfL28fIiSDPXYs0mias',
        'X-Naver-Client-Secret': 'QFImDfwoR0'
    }
    data = {
        'source': 'ko',
        'target': 'en',
        'text': text
    }
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    return result['message']['result']['translatedText']


def dall_e(eng_text):
    url = 'https://main-dalle-server-scy6500.endpoint.ainize.ai/generate'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = '{"text": "%s", "num_images": 3}' % eng_text
    response = requests.post(url, headers=headers, data=data)
    # result = response.json()
    return response


def make_audio(text):
    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    key = '43fdc9455b281f774ea7f7c850fa57ba'
    headers = {
        "Content-Type": "application/xml",
        "Authorization": "KakaoAK " + key,
    }
    data = f'<speak> \
    <voice name="WOMAN_READ_CALM"> \
    <prosody rate="slow" volume="loud">{text}</prosody> \
    </voice></speak>'.encode('utf-8')
    # data = f"<speak> {text}</speak>".encode('utf-8')
    res = requests.post(url, headers=headers, data=data)
    with open(f"static/tts_file/{text}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(res.content)
    # f = open('ㅎㅎㅎ.wav', 'wb')
    # f.write(res.content)
    # f.close()
