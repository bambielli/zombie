from django.shortcuts import render, redirect
import os
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))
# Create your views here.

def zombie_on(request):
	r.set('zombie', 'Yes')
	return redirect('index')

def zombie_off(request):
	r.set('zombie', 'No')
	return redirect('index')

def index(request):
	zombie = r.get('zombie') or 'No'
	return render(request, 'index.html', {'zombie': zombie})
