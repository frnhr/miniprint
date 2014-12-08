# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fineprint', '0004_document_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='company',
            field=models.ForeignKey(related_name='documents', to='users.Company'),
            preserve_default=True,
        ),
    ]
