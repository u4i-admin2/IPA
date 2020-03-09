# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
        """
        data migrate and map to new types
        """
        judge_file = apps.get_model("judges", "JudgeFile")
        db_alias = schema_editor.connection.alias
        judge_file.objects.using(db_alias).filter(
            file_type='ruling').update(file_type='rulings')
        judge_file.objects.using(db_alias).filter(
            file_type='verdict').update(file_type='verdicts')
        judge_file.objects.using(db_alias).filter(
            file_type='transcript').update(file_type='transcripts')
        judge_file.objects.using(db_alias).filter(
            file_type='image').update(file_type='campaigns')


class Migration(migrations.Migration):

    dependencies = [
        ('judges', '0008_auto_20150723_1143'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
