# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core_types.fields


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0025_auto_20150917_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonerarrest',
            name='partial_date',
            field=core_types.fields.PartialDateField(null=True),
            preserve_default=True,
        ),
    ]
