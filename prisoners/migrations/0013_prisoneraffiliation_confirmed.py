# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0012_auto_20150528_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoneraffiliation',
            name='confirmed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
