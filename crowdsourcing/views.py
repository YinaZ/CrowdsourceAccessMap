from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Data, CustomUser, Intersection
from .forms import UserForm, AuthenticationForm
import json
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

def ranking(request):
    template = loader.get_template('ranking.html')

    users = []
    for user in CustomUser.objects.all().order_by('-rank'):
        users.append(user)
    context = {'users': users, }
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                user = CustomUser.objects.get(username=request.POST['username'])
            except CustomUser.DoesNotExist:
                user = CustomUser()
                user.username = request.POST['username']
                user.age = request.POST['age']
                user.save()
                django_login(request, user)
                return redirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthenticationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            try: 
                user = CustomUser.objects.get(username=request.POST['username'])
            except CustomUser.DoesNotExist:
                user = None
            if user is not None:
                django_login(request, user)
                return redirect('/')
            form = AuthenticationForm()
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    django_logout(request)
    template  = loader.get_template('logged_out.html')
    context = {}
    return HttpResponse(template.render(context, request))

def leaflet(request):
    template = loader.get_template('crowdsourcing/leaflet.html')
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def getCoordinates(request):
    if request.method != 'GET':
        return redirect('/')
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return redirect('/')
    response = {}
    # data = Data.objects.all()[0]
    # response['coordinates'] = data.geom['coordinates']
    for intersection in (Intersection.objects.all()):
        if (not (Data.objects.filter(user__username=username, intersection=intersection))):
            response['coordinates'] = intersection.geom['coordinates']
            return HttpResponse(json.dumps(response), content_type="application/json")
    response['coordinates'] = Intersection.objects.all()[0].geom['coordinates']
    return HttpResponse(json.dumps(response), content_type="application/json")

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
