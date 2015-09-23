from django.conf.urls import url
import os
from . import views

zombie_on = os.environ.get('zombie_on')
zombie_off = os.environ.get('zombie_off')

urlpatterns = [
	url(zombie_on, views.zombie_on, name='zombie_on'),
	url(zombie_off, views.zombie_off, name='zombie_off'),
	url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
	url(r'^$', views.index, name='index'),
]