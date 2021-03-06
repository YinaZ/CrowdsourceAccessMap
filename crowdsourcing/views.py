from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Data, CustomUser, Intersection
from .forms import UserForm, AuthenticationForm
import json
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from .settings import MEDIA_ROOT
import csv
from django.utils import timezone

def ranking(request):
    template = loader.get_template('ranking.html')

    users = []
    for user in CustomUser.objects.all().order_by('-rank'):
        users.append(user)
    context = {'users': users, }
    return HttpResponse(template.render(context, request))

def hrRanking(request):
    template = loader.get_template('hourly_ranking.html')
    users = []
    now = timezone.localtime(timezone.now())
    for user in CustomUser.objects.all():
        user.hr_rank = 0
        for data in Data.objects.filter(user=user, date__hour=now.hour, date__day=now.day, date__month=now.month, date__year=now.year):
            user.hr_rank += data.intersection.rank
        user.save()
    for user in CustomUser.objects.all().order_by('-hr_rank'):
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

def getCoordinates(request):
    if request.method != 'GET':
        return redirect('/')
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return redirect('/')
    response = {}
    for intersection in (Intersection.objects.all()):
        if (not (Data.objects.filter(user__username=username, intersection=intersection))):
            response['coordinates'] = intersection.geom['coordinates']
            response['id'] = intersection.id
            return HttpResponse(json.dumps(response), content_type="application/json")
    intersection = Intersection.objects.all()[0]
    response['coordinates'] = intersection.geom['coordinates']
    response['id'] = intersection.id
    return HttpResponse(json.dumps(response), content_type="application/json")

def addElement(request):
    if request.method != 'POST':
        return redirect('home')
    body = json.loads(request.body)
    id = body['intersection']
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return redirect('/')
    intersection = Intersection.objects.filter(id=id)[0]
    user = CustomUser.objects.filter(username=username)[0]
    data = Data()
    if (body['correct'] == 1):
        data.geom = json.loads(body['geom'])
    else:
        data.correct = False
    data.sidewalks = body['sidewalks']
    data.user = user
    data.intersection = intersection
    data.date = timezone.now()
    data.save()
    user.rank += intersection.rank
    user.save()
    return HttpResponse("OK")

def deleteElement(request):
    if request.method != 'POST':
        return redirect('home')
    body = json.loads(request.body)
    id = request.META['HTTP_INTERSECTION']
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return redirect('/')
    intersection = Intersection.objects.filter(id=id)[0]
    user = CustomUser.objects.filter(username=username)[0]
    data = Data.objects.filter(geom=body, user=user, intersection=intersection)
    if not data:
        return HttpResponseBadRequest()
    data.delete()
    user.rank -= intersection.rank
    user.save()
    return HttpResponse("OK")
