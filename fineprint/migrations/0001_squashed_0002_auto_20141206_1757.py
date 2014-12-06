# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'fineprint', '0001_initial'), (b'fineprint', '0002_auto_20141206_1757')]

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, b'Heading'), (1, b'Paragraph')])),
                ('text', models.TextField()),
                ('heading_strength', models.PositiveSmallIntegerField(choices=[(0, b'H1'), (1, b'H2'), (2, b'H3'), (3, b'H4'), (4, b'H5'), (5, b'H6')])),
                ('previous', models.OneToOneField(related_name='next', null=True, blank=True, to='fineprint.Chunk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinePrint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('company', models.ForeignKey(to='users.Company')),
                ('first_chunk', models.OneToOneField(related_name='fineprint', to='fineprint.Chunk')),
            ],
            options={
                'verbose_name': 'Legal Text',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='heading_strength',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(0, b'H1'), (1, b'H2'), (2, b'H3'), (3, b'H4'), (4, b'H5'), (5, b'H6')]),
            preserve_default=True,
        ),
    ]
