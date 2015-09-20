from django import forms
from django.forms import ModelForm

from scraper.models import Email

class EmailForm(ModelForm):
	class Meta:
		model = Email
		fields = ['email']
		widgets = {
			'email': forms.EmailInput(attrs={'placeholder': 'Enter Email Address'})
		}