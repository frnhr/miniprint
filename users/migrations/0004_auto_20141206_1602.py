# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(default=None, max_length=50, unique=True, null=True),
            preserve_default=True,
        ),
    ]
