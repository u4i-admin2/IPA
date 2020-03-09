# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0005_auto_20150513_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonerdetention',
            name='detention_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Detention Type', choices=[(b'detained_before_sentencing', 'Detained before Sentencing'), (b'sentenced', 'Sentenced'), (b'transferred', 'Transferred')]),
            preserve_default=True,
        ),
    ]
