# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0017_prisoner_latest_activity_persecuted_for_name_fa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonerfile',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'prisoner_activism', "Prisoner's activism"), (b'court', 'Court'), (b'media', 'Media'), (b'family', 'Family'), (b'campaigns', 'Campaigns')]),
            preserve_default=True,
        ),
    ]
