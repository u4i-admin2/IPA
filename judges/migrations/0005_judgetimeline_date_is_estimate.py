# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0004_auto_20150521_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgetimeline',
            name='date_is_estimate',
            field=models.NullBooleanField(verbose_name='Timeline Date Is Estimate?'),
            preserve_default=True,
        ),
    ]
