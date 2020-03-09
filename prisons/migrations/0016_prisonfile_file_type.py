# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0015_prison_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonfile',
            name='file_type',
            field=models.CharField(default=b'uncategorized', max_length=16, choices=[(b'visual_records', 'Visual records'), (b'mistreatments', 'Mistreatments'), (b'testimonials', 'Testimonials'), (b'campaigns', 'Campaigns'), (b'uncategorized', 'Uncategorized')]),
            preserve_default=True,
        ),
    ]
