# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0003_auto_20141206_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='vote_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='vote_type',
        ),
    ]
