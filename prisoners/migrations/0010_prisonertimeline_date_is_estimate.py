# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0009_auto_20150521_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonertimeline',
            name='date_is_estimate',
            field=models.NullBooleanField(verbose_name='Timeline Date Is Estimate?'),
            preserve_default=True,
        ),
    ]
