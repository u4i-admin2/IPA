# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0014_auto_20150701_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='latest_sentenced_judge_name_en',
            field=models.TextField(null=True, verbose_name='Judge name of most recent sentence of most recent arrest (cached for search results)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='latest_sentenced_judge_name_fa',
            field=models.TextField(null=True, verbose_name='Judge name of most recent sentence of most recent arrest (cached for search results)', blank=True),
            preserve_default=True,
        ),
    ]
