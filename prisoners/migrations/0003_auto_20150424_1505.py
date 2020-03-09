# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0002_auto_20150424_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prisonerdetention',
            name='social_depravation',
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_day',
            field=models.IntegerField(null=True, verbose_name='Detention Day (Gregorian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_day_fa',
            field=models.IntegerField(null=True, verbose_name='Detention Day (Persian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_is_approx',
            field=models.BooleanField(default=False, verbose_name='Detention date is approximate?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_month',
            field=models.IntegerField(null=True, verbose_name='Detention Month (Gregorian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_month_fa',
            field=models.IntegerField(null=True, verbose_name='Detention Month (Persian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_type',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Detention Type', choices=[(b'detained_before_sentencing', 'Detained before Sentencing'), (b'sentenced', 'Sentenced'), (b'transferred', 'Transferred')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_year',
            field=models.IntegerField(null=True, verbose_name='Detention Year (Gregorian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonerdetention',
            name='detention_year_fa',
            field=models.IntegerField(null=True, verbose_name='Detention Year (Persian)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonersentence',
            name='social_depravation',
            field=models.TextField(null=True, verbose_name='Social Deprivation', blank=True),
            preserve_default=True,
        ),
    ]
