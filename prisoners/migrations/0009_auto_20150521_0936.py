# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0008_auto_20150521_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='biography',
            field=models.TextField(null=True, verbose_name='Biography', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='biography_en',
            field=models.TextField(null=True, verbose_name='Biography', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='biography_fa',
            field=models.TextField(null=True, verbose_name='Biography', blank=True),
            preserve_default=True,
        ),
    ]
