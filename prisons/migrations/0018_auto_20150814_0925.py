# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
        """
        data migrate and map to new types
        """
        prison_file = apps.get_model("prisons", "PrisonFile")
        db_alias = schema_editor.connection.alias
        prison_file.objects.using(db_alias).filter(
            file_type='uncategorized').update(file_type='visual_records')


class Migration(migrations.Migration):

    dependencies = [
        ('prisons', '0017_auto_20150723_1141'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
