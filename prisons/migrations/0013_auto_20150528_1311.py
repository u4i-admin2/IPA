# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0012_auto_20150528_1259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prisonfacilitylink',
            old_name='Facility',
            new_name='facility',
        ),
    ]
