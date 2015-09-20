from django.shortcuts import render, redirect
from django.core.mail.message import EmailMessage
from scraper.models import Email
import os
import redis
from zombie.settings import EMAIL_HOST_USER
from scraper.forms.model_forms import EmailForm
from django.http import HttpResponseRedirect


r = redis.StrictRedis.from_url(os.environ.get("REDIS_URL"))

def zombie_on(request):
	current_zombie_state = r.get('zombie')
	print "current zombie state is:"
	print current_zombie_state
	if current_zombie_state != 'Yes':
		#if zombie is not already 'Yes', then set it and send emails
		print "Turning zombie on (state must have been No)"
		r.set('zombie', 'Yes')
		email_qset = Email.objects.all()
		emails = [email.email for email in email_qset]
		emails_to_send = EmailMessage('Zombie is in stock!', 'That sweet zombie nectar is in stock. Go get it!', EMAIL_HOST_USER, [], emails)
		emails_to_send.send(fail_silently=False)
	#if it was already 'yes', then just render index
	return redirect('index')

def zombie_off(request):
	current_zombie_state = r.get('zombie')
	print "current zombie state is:"
	print current_zombie_state
	if current_zombie_state != 'No':
		print "Turning zombie off (state must have been Yes)"
		r.set('zombie', 'No')
		email_qset = Email.objects.all()
		emails = [email.email for email in email_qset] #emails in the database
		#create an EmailMessage so you can use BCC
		emails_to_send = EmailMessage('Floyds just ran out of zombie...', 'Zombie just ran out of stock at floyds...maybe next time!', EMAIL_HOST_USER, [], emails)
		#send the EmailMessage
		emails_to_send.send(fail_silently=False)

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
