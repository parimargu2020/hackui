from django.shortcuts import render

from django.http import HttpResponse
import requests
import json

REST_API_ENDPOINT = "http://localhost:8001/api/"

# MVT
# M - Model
# V - View - Controller(vs MVC)
# T - Template(Html, Css, Js)

# MVC
# M - Model
# V - View(Html, Css, Js)
# C - Controller - View(Django)


# Create your views here.
def name_pronunciation(request):
    if request.method == 'POST':
        name_text = request.POST.get('name_text')
        print(name_text)

        name_input_data = { "name_text": name_text, "audio_file": "" }

        headers = {'Content-type': 'application/json'}

        # Convert post input data/request and get the reponse data
        # Post data to REST API
        response = requests.post(url=REST_API_ENDPOINT, data=json.dumps(name_input_data), headers=headers)
        print(response)
        name_pronunciation = response.json()
        print(name_pronunciation)

        return render(request, "home.html", {"name_pronunciation": name_pronunciation})
    else:
        return render(request, "home.html")