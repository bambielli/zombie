from django.shortcuts import render, redirect
from django.core.mail import send_mail
from scraper.models import Email
import os
import redis
from zombie.settings import EMAIL_HOST_USER
from scraper.forms.model_forms import EmailForm
from django.http import HttpResponseRedirect


r = redis.StrictRedis.from_url(os.environ.get("REDIS_URL"))

# Create your views here.
def zombie_on(request):
	r.set('zombie', 'Yes')
	email_qset = Email.objects.all()
	import pdb
	pdb.set_trace()
	emails = [email.email for email in email_qset]
	send_mail('Zombie is in stock!', 'That sweet zombie nectar is in stock. go get it!', EMAIL_HOST_USER, emails, fail_silently=False)
	return redirect('index')

def zombie_off(request):
	r.set('zombie', 'No')
	return redirect('index')

def index(request):
	zombie = r.get('zombie') or 'No'
	messages = ''
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = EmailForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			Email.objects.create(email=form.cleaned_data['email'])
			messages = 'Your email was successfully submitted'
	else:
		form = EmailForm()

	return render(request, 'index.html', {'zombie': zombie, 'form': form, 'messages': messages})
