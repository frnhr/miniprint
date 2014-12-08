# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fineprint', '0003_auto_20141207_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 7, 21, 41, 9, 91770, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
