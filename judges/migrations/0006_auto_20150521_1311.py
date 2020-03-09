# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0005_judgetimeline_date_is_estimate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='judgetimeline',
            old_name='date_is_estimate',
            new_name='timeline_is_estimate',
        ),
    ]
