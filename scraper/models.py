from django.db import models
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.urlresolvers import reverse

# Create your models here.

class Email(models.Model):
	email = models.EmailField(verbose_name='email address', max_length=254, unique=True, db_index=True,
	  help_text='')

	def create_unsubscribe_link(self):
		email, token = self.make_token().split(":", 1)
		return reverse('unsubscribe',
					   kwargs={'email': email, 'token': token,})

	def make_token(self):
		return TimestampSigner().sign(self.email)

	def check_token(self, token):
		try:
			key = '%s:%s' % (self.email, token)
			TimestampSigner().unsign(key, max_age=60 * 60 * 24 * 7) # Valid for 1 week
		except (BadSignature, SignatureExpired):
			return False
		return True
