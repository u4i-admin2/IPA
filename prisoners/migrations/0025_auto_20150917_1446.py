# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0024_auto_20150904_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonersentence',
            name='judge',
            field=models.ForeignKey(verbose_name='Judge', blank=True, to='judges.Judge', null=True),
            preserve_default=True,
        ),
    ]
