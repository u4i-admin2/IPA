# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0016_prisonfile_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisonfile',
            name='file_type',
            field=models.CharField(max_length=16, choices=[(b'visual_records', 'Visual records'), (b'mistreatments', 'Mistreatments'), (b'testimonials', 'Testimonials'), (b'campaigns', 'Campaigns')]),
            preserve_default=True,
        ),
    ]
