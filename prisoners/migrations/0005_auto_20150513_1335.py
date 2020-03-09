# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0004_auto_20150507_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='latest_activity_persecuted_for_name_en',
            field=models.TextField(null=True, verbose_name='Most recent arrest (cached for search results)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='latest_detention_status_name_en',
            field=models.TextField(null=True, verbose_name='Most recent sentence of most recent arrrest, if any (cached for search results)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='latest_prison_name_en',
            field=models.TextField(null=True, verbose_name='Prison of most recent detention of most recent arrest (cached for search results)', blank=True),
            preserve_default=True,
        ),
    ]
