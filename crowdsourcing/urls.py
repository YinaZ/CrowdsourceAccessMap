from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls import include
from djgeojson.views import GeoJSONLayerView
from .models import Data

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^leaflet/$', views.leaflet, name='leaflet'),
    url(r'^register/$', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    ), name='register'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Data), name='data'),
    url(r'^addElement/$', views.addElement, name='addElement'),
    url(r'^deleteElement/$', views.deleteElement, name='deleteElement'),
#    url('^accounts/', include('django.contrib.auth.urls')),
]
