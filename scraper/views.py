from django.shortcuts import render, redirect
from django.core.mail import send_mail
import os
import redis
from zombie.settings import EMAIL_HOST_USER

r = redis.StrictRedis.from_url(os.environ.get("REDIS_URL"))# Create your views here.

def zombie_on(request):
	r.set('zombie', 'Yes')
	send_mail('Zombie is in stock!', 'That sweet zombie nectar is in stock. go get it!', EMAIL_HOST_USER, ['brian.ambielli@gmail.com'], fail_silently=False)
	return redirect('index')

def zombie_off(request):
	r.set('zombie', 'No')
	return redirect('index')

def index(request):
	zombie = r.get('zombie') or 'No'
	return render(request, 'index.html', {'zombie': zombie})
