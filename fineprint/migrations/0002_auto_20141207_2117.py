# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fineprint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_created=True)),
                ('document', models.ForeignKey(to='fineprint.Document')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='document',
            field=models.ForeignKey(related_name='chunks', to='fineprint.Document'),
            preserve_default=True,
        ),
    ]
