from django.db import models

# Create your models here.

class Email(models.Model):
	email = models.EmailField(verbose_name='email address', max_length=254, unique=True, db_index=True,
      help_text='')
