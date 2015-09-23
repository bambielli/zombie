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
	"""
	Changes the zombie state from No to Yes
	"""
	current_zombie_state = r.get('zombie')

	if current_zombie_state.decode("utf-8") != 'Yes':
		#if zombie is not already 'Yes', then set it and send emails
		r.set('zombie', 'Yes')
		email_qset = Email.objects.all()
		emails = [email.email for email in email_qset]
		emails_to_send = EmailMessage('Zombie is in stock!', 'That sweet zombie nectar is in stock. Go get it!', EMAIL_HOST_USER, [], emails)
		emails_to_send.send(fail_silently=False)

	#if it was already 'yes', then just redirect to index
	return redirect('index')

def zombie_off(request):
	"""
	Changes the zombie state from Yes to No
	"""
	current_zombie_state = r.get('zombie')

	if current_zombie_state.decode("utf-8") != 'No':
		#If zombie is not already 'No', then set it and send emails.
		r.set('zombie', 'No')
		email_qset = Email.objects.all()
		emails = [email.email for email in email_qset] #emails in the database
		#create an EmailMessage so you can use BCC
		emails_to_send = EmailMessage('Floyds just ran out of zombie...', 'Zombie just ran out of stock at floyds...maybe next time!', EMAIL_HOST_USER, [], emails)
		#send the EmailMessage
		emails_to_send.send(fail_silently=False)

	#if it was already no, then just redirect to index
	return redirect('index')

def unsubscribe(request):
	"""
	This view is used to process response from a user who wishes to unsubscribe from the app.
	"""
	messages = ''

	# If response is post, user has submitted an email to be deleted from our system
	if request.method == 'POST':
		form = EmailForm(request.POST)

		# Confirm a valid submission to the form
		if form.is_valid():

			email_to_delete = Email.objects.filter(email=form.cleaned_data['email'])

			if len(email_to_delete) > 0: #if an email was found...
				email_to_delete.delete() #...delete the email
				messages = "You have successfully unsubscribed"
			else: #else, push a response that we do not have record of that email in our system.s
				messages = "That email does not exist in our systems. Please contact us if you think this is incorrect!"

	else: #else it was just a normal get to the url, and we should render the unsubscribe form
		form = EmailForm()

	return render(request, 'unsubscribe.html', {'form': form, 'messages': messages})

def index(request):
	zombie = r.get('zombie') or 'No'
	messages = ''

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = EmailForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			Email.objects.create(email=form.cleaned_data['email'])
			messages = "Your email was successfully submitted"
	else:
		form = EmailForm()

	return render(request, 'index.html', {'zombie': zombie, 'form': form, 'messages': messages})
