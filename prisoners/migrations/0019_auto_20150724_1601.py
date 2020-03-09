# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0018_auto_20150723_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisoner',
            name='ethnicity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Ethnicity', blank=True, to='core_types.Ethnicity', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='religion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Religion', blank=True, to='core_types.Religion', null=True),
            preserve_default=True,
        ),
    ]
