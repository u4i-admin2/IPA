# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    """
    force update publish parts of profile
    """
    prisoner_arrest = apps.get_model("prisoners", "PrisonerArrest")
    prisoner_detention = apps.get_model("prisoners", "PrisonerDetention")
    prisoner_sentence = apps.get_model("prisoners", "PrisonerSentence")
    sentence_behaviour = apps.get_model("prisoners", "SentenceBehaviour")

    db_alias = schema_editor.connection.alias

    prisoner_arrest.objects.using(db_alias).all().update(is_published=True)
    prisoner_detention.objects.using(db_alias).all().update(is_published=True)
    prisoner_sentence.objects.using(db_alias).all().update(is_published=True)
    sentence_behaviour.objects.using(db_alias).all().update(is_published=True)


class Migration(migrations.Migration):

    dependencies = [
        ('prisoners', '0022_auto_20150805_1028'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
