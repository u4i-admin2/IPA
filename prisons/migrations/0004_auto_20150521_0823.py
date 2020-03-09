# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0003_auto_20150513_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonquote',
            name='source',
            field=models.CharField(max_length=255, null=True, verbose_name='Source', blank=True),
            preserve_default=True,
        ),
    ]
