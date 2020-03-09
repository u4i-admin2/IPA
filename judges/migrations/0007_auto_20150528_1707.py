# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0006_auto_20150521_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgesource',
            name='link',
            field=models.CharField(max_length=255, null=True, verbose_name='Link', blank=True),
            preserve_default=True,
        ),
    ]
