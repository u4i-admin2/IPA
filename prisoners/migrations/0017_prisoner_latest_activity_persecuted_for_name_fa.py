# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0016_auto_20150722_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='latest_activity_persecuted_for_name_fa',
            field=models.TextField(null=True, verbose_name='Most recent activity (cached for search results)', blank=True),
            preserve_default=True,
        ),
    ]
