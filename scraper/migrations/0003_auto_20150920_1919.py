# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20150920_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(help_text=b'', unique=True, max_length=254, verbose_name=b'email address', db_index=True),
        ),
    ]
