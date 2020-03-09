# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='detention_day',
            field=models.IntegerField(null=True, verbose_name='Detention Day (Gregorian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='detention_day_fa',
            field=models.IntegerField(null=True, verbose_name='Detention Day (Persian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='detention_is_approx',
            field=models.BooleanField(default=False, verbose_name='Detention date is approximate?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='detention_month',
            field=models.IntegerField(null=True, verbose_name='Detention Month (Gregorian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='detention_month_fa',
            field=models.IntegerField(null=True, verbose_name='Detention Month (Persian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='detention_year',
            field=models.IntegerField(null=True, verbose_name='Detention Year (Gregorian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='detention_year_fa',
            field=models.IntegerField(null=True, verbose_name='Detention Year (Persian)', blank=True),
            preserve_default=True,
        ),
    ]
