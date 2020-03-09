# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0007_auto_20150528_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prisonfacilitylink',
            name='facility_id',
        ),
        migrations.RemoveField(
            model_name='prisonfacilitylink',
            name='prison_id',
        ),
        migrations.DeleteModel(
            name='PrisonFacilityLink',
        ),
        migrations.AddField(
            model_name='prison',
            name='facilities',
            field=models.ManyToManyField(to='prisons.PrisonFacility', null=True, verbose_name='Prison Facility', blank=True),
            preserve_default=True,
        ),
    ]
