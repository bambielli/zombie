from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail.message import EmailMultiAlternatives
from scraper.models import Email
import os
import redis
from zombie.settings import EMAIL_HOST_USER
from scraper.forms.model_forms import EmailForm

r = redis.StrictRedis.from_url(os.environ.get("REDIS_URL"))


def _send_email(subject, msg_to_send, host, email_qset):
	"""
	Takes the subject, text body, host and qset of email objects
	sends emails to each of the emails in email_qset, creating a unique unsubscribe link for each.
	"""
	for email in email_qset:
		unsub_link = 'http://'+ host + email.create_unsubscribe_link()
		html_content = '<p>'+msg_to_send+'</p></br><a href="'+unsub_link+'">click here to unsubscribe</a>'
		email_to_send = EmailMultiAlternatives(subject, msg_to_send, EMAIL_HOST_USER, [email.email])
		email_to_send.attach_alternative(html_content, "text/html")
		email_to_send.msg_subtype = 'html'
		email_to_send.send(fail_silently=False)

def zombie_on(request):
	"""
	Changes the zombie state from No to Yes
	Sends email if the state has changed.
	"""
	current_zombie_state = r.get('zombie')
	if current_zombie_state.decode("utf-8") != 'Yes':
		#if zombie is not already 'Yes', then set it and send emails
		r.set('zombie', 'Yes')

		subject = 'Zombie is in stock!'
		text_content = 'That sweet Zombie nectar is in stock. Go get it!'
		host = request.get_host()
		email_qset = Email.objects.all()

		_send_email(subject, text_content, host, email_qset)

	#if it was already 'yes', then just redirect to index
	return redirect('index')

def zombie_off(request):
	"""
	Changes the zombie state from Yes to No
	Sends email if the state has changed.
	"""
	current_zombie_state = r.get('zombie')
	if current_zombie_state.decode("utf-8") != 'No':
		#If zombie is not already 'No', then set it and send emails.
		r.set('zombie', 'No')

		subject = 'Floyds just ran out of zombie...'
		text_content = 'Zombie just ran out of stock at floyds...maybe next time!'
		host = request.get_host()
		email_qset = Email.objects.all()

		_send_email(subject, text_content, host, email_qset)

	#if it was already no, then just redirect to index
	return redirect('index')

def unsubscribe(request, email, token):
	"""
	This view is used by the link in the emails that are sent out to unsubscribe users
	"""
	email = get_object_or_404(Email, email=email)
	success = ''
	error = ''
	if email.check_token(token):
		# unsubscribe them
		email.delete()
		success = "You successfully unsubscribed"
	else:
		errors = "invalid token. try again"

	return render(request, 'unsubscribe.html', {'success':success, 'error': error})

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
