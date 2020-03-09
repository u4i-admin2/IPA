# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
        """
        set any records with 'video', 'picture', 'pdf' to prisoner_activism
        """
        prisoner_file = apps.get_model("prisoners", "PrisonerFile")
        db_alias = schema_editor.connection.alias
        prisoner_file.objects.using(db_alias).filter(
            file_type='pdf').update(file_type='prisoner_activism')
        prisoner_file.objects.using(db_alias).filter(
            file_type='video').update(file_type='prisoner_activism')
        prisoner_file.objects.using(db_alias).filter(
            file_type='picture').update(file_type='prisoner_activism')


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0019_auto_20150724_1601'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
