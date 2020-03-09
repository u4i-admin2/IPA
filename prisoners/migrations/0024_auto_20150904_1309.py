# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0023_auto_20150817_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonersentence',
            name='fine',
            field=models.BigIntegerField(null=True, verbose_name='Fine (Rials)', blank=True),
            preserve_default=True,
        ),
    ]
