# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judgeposition',
            options={'ordering': ('started_year', 'started_month', 'started_day'), 'verbose_name': 'Position'},
        ),
        migrations.AddField(
            model_name='judgequote',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judgequote',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judgequote',
            name='name_fa',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
