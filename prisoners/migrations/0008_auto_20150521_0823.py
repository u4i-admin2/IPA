# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0007_prisonerrelationship_is_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonerquote',
            name='source',
            field=models.CharField(max_length=255, null=True, verbose_name='Source', blank=True),
            preserve_default=True,
        ),
    ]
