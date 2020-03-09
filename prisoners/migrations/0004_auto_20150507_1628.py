# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0003_auto_20150424_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonerquote',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prisonerquote',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerquote',
            name='name_fa',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
