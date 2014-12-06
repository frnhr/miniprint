# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fineprint', '0001_initial'),
        ('discuss', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='chunk',
            field=models.ForeignKey(related_name='comments', blank=True, to='fineprint.Chunk', null=True),
            preserve_default=True,
        ),
    ]
