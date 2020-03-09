# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from datetime import datetime


def forwards_func(apps, schema_editor):
        """
        force update prisoners to trigger save signal and updated processes
        """
        prisoner = apps.get_model("prisoners", "Prisoner")
        now = datetime.now()
        db_alias = schema_editor.connection.alias

        prisoner.objects.using(db_alias).all().update(updated=now)


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0020_auto_20150804_1615'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
