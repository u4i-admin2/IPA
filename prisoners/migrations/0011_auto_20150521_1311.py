# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0010_prisonertimeline_date_is_estimate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prisonertimeline',
            old_name='date_is_estimate',
            new_name='timeline_is_estimate',
        ),
    ]
