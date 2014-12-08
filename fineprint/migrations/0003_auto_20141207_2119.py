# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fineprint', '0002_auto_20141207_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentagreement',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
