# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0014_auto_20150528_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='prison',
            name='picture',
            field=models.ImageField(upload_to=b'prison_pics', null=True, verbose_name='Prison Picture', blank=True),
            preserve_default=True,
        ),
    ]
