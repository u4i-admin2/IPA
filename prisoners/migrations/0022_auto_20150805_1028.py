# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0021_auto_20150805_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonersentence',
            name='exiled',
            field=models.BooleanField(default=False, verbose_name='Exiled'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonersentence',
            name='life',
            field=models.BooleanField(default=False, verbose_name='Life'),
            preserve_default=True,
        ),
    ]
