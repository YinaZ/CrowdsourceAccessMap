from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls import include
from djgeojson.views import GeoJSONLayerView
from .models import Data, CustomUser, Intersection
from .forms import UserForm
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^leaflet/$', views.leaflet, name='leaflet'),
    url(r'^register/$', views.register, name='register'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Intersection), name='data'),
    url(r'^addElement/$', views.addElement, name='addElement'),
    url(r'^deleteElement/$', views.deleteElement, name='deleteElement'),
    url(r'^ranking/$', views.ranking, name='ranking'),
    url(r'^getCoordinates/$', views.getCoordinates, name='getCoordinates'),
#    url('^accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
