# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0006_auto_20150513_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonerrelationship',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='Alleged or confirmed?'),
            preserve_default=True,
        ),
    ]
