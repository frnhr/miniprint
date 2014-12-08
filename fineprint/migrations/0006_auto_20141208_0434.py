# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fineprint', '0005_auto_20141208_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentagreement',
            name='document',
            field=models.ForeignKey(related_name='agreements', to='fineprint.Document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentagreement',
            name='user',
            field=models.ForeignKey(related_name='agreements', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
