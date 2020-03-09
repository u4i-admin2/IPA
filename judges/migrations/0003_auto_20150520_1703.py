# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0002_auto_20150507_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='judge_type',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Judge Type', choices=[(None, 'Unknown'), (b'research', 'Research'), (b'primary', 'Primary'), (b'appeal', 'Appeal'), (b'supreme', 'Supreme')]),
            preserve_default=True,
        ),
    ]
