# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fineprint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='previous',
            field=models.OneToOneField(related_name='next', null=True, to='fineprint.Element'),
            preserve_default=True,
        ),
    ]
