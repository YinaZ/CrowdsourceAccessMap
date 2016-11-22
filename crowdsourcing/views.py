from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

def leaflet(request):
    template = loader.get_template('crowdsourcing/leaflet.html')
    context = {}
    return HttpResponse(template.render(context, request))
