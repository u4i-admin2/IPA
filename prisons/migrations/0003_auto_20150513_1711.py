# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0002_auto_20150507_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='prison',
            name='bio',
            field=models.TextField(null=True, verbose_name='Bio', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prison',
            name='bio_en',
            field=models.TextField(null=True, verbose_name='Bio', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prison',
            name='bio_fa',
            field=models.TextField(null=True, verbose_name='Bio', blank=True),
            preserve_default=True,
        ),
    ]
