# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0013_prisoneraffiliation_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonersentence',
            name='social_depravation_en',
            field=models.TextField(null=True, verbose_name='Social Deprivation', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonersentence',
            name='social_depravation_fa',
            field=models.TextField(null=True, verbose_name='Social Deprivation', blank=True),
            preserve_default=True,
        ),
    ]
