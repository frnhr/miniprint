# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('user', models.OneToOneField(related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('element_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fineprint.Element')),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=('fineprint.element',),
        ),
        migrations.CreateModel(
            name='FinePrint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('company', models.ForeignKey(to='fineprint.Company')),
            ],
            options={
                'verbose_name': 'Legal Text',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('element_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fineprint.Element')),
                ('strength', models.PositiveSmallIntegerField(choices=[(0, b'h1'), (1, b'h2'), (2, b'h3'), (3, b'h4'), (4, b'h5'), (5, b'h6')])),
                ('text', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=('fineprint.element',),
        ),
        migrations.AddField(
            model_name='fineprint',
            name='first_element',
            field=models.OneToOneField(related_name='fineprint', to='fineprint.Element'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='previous',
            field=models.OneToOneField(related_name='next', to='fineprint.Element'),
            preserve_default=True,
        ),
    ]
