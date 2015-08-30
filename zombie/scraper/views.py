from django.shortcuts import render, redirect
import os
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
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
