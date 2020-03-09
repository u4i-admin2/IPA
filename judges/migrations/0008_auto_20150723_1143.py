# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0007_auto_20150528_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgefile',
            name='file_type',
            field=models.CharField(max_length=16, choices=[(b'rulings', 'Rulings'), (b'verdicts', 'Verdicts'), (b'transcripts', 'Transcripts'), (b'campaigns', 'Campaigns')]),
            preserve_default=True,
        ),
    ]
