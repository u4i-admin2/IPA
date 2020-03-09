# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core_types.utils
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prisons', '0011_auto_20150528_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisonfacilitylink',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 12, 59, 14, 672144, tzinfo=utc), verbose_name='Created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prisonfacilitylink',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=core_types.utils.get_request_user, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Created By'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonfacilitylink',
            name='is_published',
            field=models.BooleanField(default=False, db_index=True, verbose_name='Approved for publishing?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisonfacilitylink',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 12, 59, 22, 389875, tzinfo=utc), verbose_name='Last Updated', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prisonfacilitylink',
            name='updated_by',
            field=models.ForeignKey(related_name='+', verbose_name='Last Updated By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
