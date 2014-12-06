# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0002_comment_chunk'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='vote_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='vote_type',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'chunk', b'Chunk'), (b'comment', b'Comment')]),
            preserve_default=True,
        ),
    ]
