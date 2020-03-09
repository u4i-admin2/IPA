# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0010_auto_20150528_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonfacilitylink',
            name='prison',
            field=models.ForeignKey(related_name='facilitylinks', to='prisons.Prison'),
            preserve_default=True,
        ),
    ]
