# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0006_auto_20150521_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrisonFacilityLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('facility_id', models.ForeignKey(to='prisons.PrisonFacility')),
                ('prison_id', models.ForeignKey(to='prisons.Prison')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='prison',
            name='facilities',
        ),
    ]
