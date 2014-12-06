# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('chunk_type', models.PositiveSmallIntegerField(choices=[(0, b'Heading'), (1, b'Paragraph')])),
                ('text', models.TextField()),
                ('heading_strength', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(0, b'H1'), (1, b'H2'), (2, b'H3'), (3, b'H4'), (4, b'H5'), (5, b'H6')])),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
            options={
                'verbose_name': 'Legal Document',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chunk',
            name='document',
            field=models.ForeignKey(to='fineprint.Document'),
            preserve_default=True,
        ),
    ]
