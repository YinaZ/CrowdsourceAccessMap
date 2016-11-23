from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Data
import json

def leaflet(request):
    template = loader.get_template('crowdsourcing/leaflet.html')
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def addElement(request):
    if request.method != 'POST':
        return redirect('home')
    data = Data()
    data.geom = json.loads(request.body)
    data.save()
    return HttpResponse("OK")

@csrf_exempt
def deleteElement(request):
    if request.method != 'POST':
        return redirect('home')
    body = json.loads(request.body)
    data = Data.objects.filter(geom=body)
    if not data:
        return HttpResponseBadRequest()
    data.delete()
    return HttpResponse("OK")
